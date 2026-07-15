"""
[INPUT]: 依赖 thirtyx.pipeline 的 provider-neutral orchestration
[OUTPUT]: 验证去重、preview 零写入与显式 execute 写入
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
        return [{"email": "new@example.com"}, {"email": "OLD@example.com"}]


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


if __name__ == "__main__":
    unittest.main()
