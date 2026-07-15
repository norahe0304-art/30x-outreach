"""
[INPUT]: 依赖 thirtyx.evaluation 与 wheel 内置 demo campaign
[OUTPUT]: 验证通过决策、无证据文案硬阻断与 terminal control-character 清理
[POS]: tests/ 的 sequence 质量门回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import unittest

from thirtyx.cli import demo_json
from thirtyx.evaluation import evaluate_sequence
from thirtyx.rendering import terminal_text


class SequenceLinterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campaign = demo_json("campaign.json")

    def test_demo_is_ready_for_review(self):
        report = evaluate_sequence(self.campaign)
        self.assertEqual(report["decision"], "READY_FOR_HUMAN_REVIEW")
        self.assertEqual(report["hard_blockers"], [])

    def test_unsupported_praise_is_blocked(self):
        campaign = copy.deepcopy(self.campaign)
        campaign["steps"][0]["body"] = "Impressive momentum — your background caught my eye."
        report = evaluate_sequence(campaign)
        self.assertEqual(report["decision"], "REVISE")
        self.assertTrue(report["hard_blockers"])

    def test_overlapping_decision_thresholds_are_blocked(self):
        campaign = copy.deepcopy(self.campaign)
        campaign["experiment"]["decision_thresholds"]["kill"]["value"] = 0.04
        report = evaluate_sequence(campaign)
        self.assertEqual(report["decision"], "REVISE")
        self.assertTrue(any("non-overlapping" in error for error in report["hard_blockers"]))

    def test_string_thresholds_are_blocked_without_crashing(self):
        campaign = copy.deepcopy(self.campaign)
        campaign["experiment"]["decision_thresholds"] = "scale above three percent"
        report = evaluate_sequence(campaign)
        self.assertEqual(report["decision"], "REVISE")

    def test_terminal_text_removes_control_characters(self):
        self.assertEqual(terminal_text("safe\x1b[31m\ntext"), "safe [31m text")


if __name__ == "__main__":
    unittest.main()
