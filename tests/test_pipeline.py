"""
[INPUT]: 依赖 thirtyx.pipeline 的 provider-neutral orchestration
[OUTPUT]: 验证去重、preview 零写入、audience-gated execute 与 plugin registry
[POS]: tests/ 的外部 destination 安全回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import unittest

from thirtyx.pipeline import DemandPipeline
from thirtyx.providers.base import ProviderInfo
from thirtyx.providers.registry import ProviderRegistry


class FakeSource:
    info = ProviderInfo("fake", "source", "Offline test source", (), False)

    def source(self, _criteria, _volume):
        verification = {
            "status": "valid", "provider": "fake", "checked_at": "2026-07-14T10:00:00Z",
            "is_free_email": False, "is_role_based": False,
        }
        signal = {
            "id": "signal-1", "observation": "A verified buying signal.",
            "source": "https://example.com/signal", "observed_at": "2026-07-14T09:00:00Z", "verified": True,
        }
        return [
            {"email": "new@example.com", "verification": verification, "signals": [signal]},
            {"email": "OLD@example.com", "verification": verification, "signals": [signal]},
        ]


class FakeVerifier:
    def verify(self, leads):
        return list(leads)


class FakeDestination:
    def __init__(self):
        self.uploads = []

    def existing_emails(self):
        return ["old@example.com"]

    def upload(self, leads, campaign_id):
        self.uploads.append((list(leads), campaign_id))
        return len(self.uploads[-1][0])


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.destination = FakeDestination()
        self.pipeline = DemandPipeline(FakeSource(), FakeVerifier(), self.destination)

    def test_preview_never_writes(self):
        result = self.pipeline.run({}, 2, "demo")
        self.assertEqual(result.ready, 1)
        self.assertEqual(result.uploaded, 0)
        self.assertEqual(self.destination.uploads, [])

    def test_execute_uploads_only_net_new_leads(self):
        result = self.pipeline.run({}, 2, "demo", execute=True)
        self.assertEqual(result.uploaded, 1)
        self.assertEqual(self.destination.uploads[0][1], "demo")

    def test_registry_returns_runnable_plugin(self):
        provider = FakeSource()
        registry = ProviderRegistry()
        registry.register(provider)
        self.assertIs(registry.get("source", "fake"), provider)

    def test_execute_rejects_leads_without_signal_proof(self):
        self.pipeline.source.source = lambda _criteria, _volume: [{
            "email": "unsafe@example.com",
            "verification": {"status": "valid", "provider": "fake", "checked_at": "2026-07-14T10:00:00Z"},
            "signals": [],
        }]
        with self.assertRaises(ValueError):
            self.pipeline.run({}, 1, "demo", execute=True)
        self.assertEqual(self.destination.uploads, [])


if __name__ == "__main__":
    unittest.main()
