"""
[INPUT]: 依赖 thirtyx.audience 与 wheel 内置 audience batch contract
[OUTPUT]: 验证 verified + signal-backed execution gate、campaign 绑定与去重
[POS]: tests/ 的 recipient 外部写入安全回归
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import unittest

from thirtyx.audience import build_audience_batch, preflight_audience
from thirtyx.cli import demo_json


class AudienceTests(unittest.TestCase):
    def setUp(self):
        self.batch = demo_json("audience.json")

    def test_accepts_verified_signal_backed_audience(self):
        self.assertEqual(preflight_audience(self.batch, "demo-ai-demand-001"), self.batch)

    def test_rejects_unverified_email(self):
        batch = copy.deepcopy(self.batch)
        batch["leads"][0]["verification"]["status"] = "unknown"
        with self.assertRaises(ValueError):
            preflight_audience(batch)

    def test_rejects_missing_signal(self):
        batch = copy.deepcopy(self.batch)
        batch["leads"][0]["signals"] = []
        with self.assertRaises(ValueError):
            preflight_audience(batch)

    def test_rejects_missing_free_or_role_classification(self):
        batch = copy.deepcopy(self.batch)
        del batch["leads"][0]["verification"]["is_role_based"]
        with self.assertRaises(ValueError):
            preflight_audience(batch)

    def test_rejects_duplicate_email(self):
        batch = copy.deepcopy(self.batch)
        batch["leads"].append(copy.deepcopy(batch["leads"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate recipient"):
            preflight_audience(batch)

    def test_build_normalizes_email(self):
        lead = copy.deepcopy(self.batch["leads"][0])
        lead["email"] = "  ALEX@NORTHSTAR.EXAMPLE "
        batch = build_audience_batch("demo-ai-demand-001", [lead], "2026-07-14T11:30:00Z")
        self.assertEqual(batch["leads"][0]["email"], "alex@northstar.example")


if __name__ == "__main__":
    unittest.main()
