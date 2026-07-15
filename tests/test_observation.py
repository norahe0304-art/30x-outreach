"""
[INPUT]: 依赖 Instantly aggregate fixture、observation adapter 与 deterministic decision engine
[OUTPUT]: 验证 campaign 绑定、rate 计算和小样本安全 guardrail 立即 KILL
[POS]: tests/ 的真实 provider result 学习闭环回归
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import copy
import tempfile
import unittest
from pathlib import Path

from thirtyx.cli import demo_json
from thirtyx.contracts import validate_instance
from thirtyx.decision import decide_experiment
from thirtyx.learning import append_record, load_records
from thirtyx.observation import observation_from_instantly


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.campaign = demo_json("campaign.json")
        self.analytics = demo_json("instantly-analytics.json")

    def observe(self, analytics=None):
        return observation_from_instantly(
            self.campaign,
            analytics or self.analytics,
            "2026-07-15T12:00:00Z",
        )

    def test_maps_aggregate_counts_to_rates(self):
        observation = self.observe()
        validate_instance(observation, "experiment-observation.schema.json")
        self.assertEqual(observation["sample_size"], 120)
        self.assertAlmostEqual(observation["metrics"]["positive_reply_rate"], 4 / 120)
        self.assertAlmostEqual(observation["metrics"]["bounce_rate"], 1 / 120)

    def test_rejects_mismatched_campaign(self):
        analytics = copy.deepcopy(self.analytics)
        analytics[0]["campaign_id"] = "other"
        with self.assertRaisesRegex(ValueError, "no row"):
            self.observe(analytics)

    def test_kills_unsafe_bounce_before_minimum_sample(self):
        analytics = copy.deepcopy(self.analytics)
        analytics[0]["new_leads_contacted_count"] = 20
        analytics[0]["bounced_count"] = 4
        observation = self.observe(analytics)
        self.assertEqual(decide_experiment(self.campaign, observation)["decision"], "KILL")

    def test_observation_can_append_to_learning_ledger(self):
        observation = self.observe()
        decision = decide_experiment(self.campaign, observation)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "learning.jsonl"
            append_record(path, self.campaign, observation, decision)
            records = load_records(path)
        self.assertEqual(records[0]["decision"]["decision"], "SCALE")


if __name__ == "__main__":
    unittest.main()
