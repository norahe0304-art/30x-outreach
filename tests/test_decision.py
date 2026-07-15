"""
[INPUT]: 依赖 thirtyx.decision 与 wheel 内置 campaign/observation
[OUTPUT]: 验证 COLLECT/SCALE/KILL/LEARN 四态决策及 identity 绑定
[POS]: tests/ 的确定性学习引擎回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import tempfile
import unittest
from pathlib import Path

from thirtyx.cli import demo_json
from thirtyx.decision import decide_experiment
from thirtyx.learning import append_record, ledger_head, load_records, verify_records


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.campaign = demo_json("campaign.json")
        self.observation = demo_json("observation.json")

    def decide(self, **metrics):
        observation = copy.deepcopy(self.observation)
        observation["metrics"].update(metrics)
        return decide_experiment(self.campaign, observation)

    def test_scale(self):
        self.assertEqual(self.decide(positive_reply_rate=0.03)["decision"], "SCALE")

    def test_kill_on_primary_metric(self):
        self.assertEqual(self.decide(positive_reply_rate=0.009)["decision"], "KILL")

    def test_kill_on_guardrail(self):
        self.assertEqual(self.decide(bounce_rate=0.03)["decision"], "KILL")

    def test_learn_between_thresholds(self):
        self.assertEqual(self.decide(positive_reply_rate=0.02)["decision"], "LEARN")

    def test_collect_before_minimum_sample(self):
        observation = copy.deepcopy(self.observation)
        observation["sample_size"] = 99
        self.assertEqual(decide_experiment(self.campaign, observation)["decision"], "COLLECT")

    def test_rejects_mismatched_observation(self):
        observation = copy.deepcopy(self.observation)
        observation["campaign_id"] = "other"
        with self.assertRaises(ValueError):
            decide_experiment(self.campaign, observation)

    def test_rejects_non_numeric_metrics(self):
        observation = copy.deepcopy(self.observation)
        observation["metrics"]["positive_reply_rate"] = "high"
        with self.assertRaises(ValueError):
            decide_experiment(self.campaign, observation)

    def test_ledger_detects_historical_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "learning.jsonl"
            decision = decide_experiment(self.campaign, self.observation)
            append_record(path, self.campaign, self.observation, decision, "2026-07-14T12:00:00+00:00")
            records = load_records(path)
            records[0]["audience"] = "mutated"
            self.assertFalse(verify_records(records)[0])

    def test_ledger_chains_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "learning.jsonl"
            decision = decide_experiment(self.campaign, self.observation)
            first = append_record(path, self.campaign, self.observation, decision, "2026-07-14T12:00:00+00:00")
            second = append_record(path, self.campaign, self.observation, decision, "2026-07-15T12:00:00+00:00")
            self.assertEqual(second["previous_sha256"], first["record_sha256"])
            records = load_records(path)
            self.assertTrue(verify_records(records)[0])
            self.assertEqual(ledger_head(records), second["record_sha256"])

    def test_ledger_rejects_recipient_fields(self):
        observation = copy.deepcopy(self.observation)
        observation["recipients"] = [{"email": "private@example.com"}]
        decision = decide_experiment(self.campaign, observation)
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            append_record(Path(directory) / "learning.jsonl", self.campaign, observation, decision)


if __name__ == "__main__":
    unittest.main()
