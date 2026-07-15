"""
[INPUT]: 依赖 wheel 内置六份 JSON Schema、demo resources 与核心 API
[OUTPUT]: 验证 campaign、observation、decision、approval、learning 跨阶段契约
[POS]: tests/ 的安装后 schema 同构回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from thirtyx.approval import create_manifest
from thirtyx.cli import demo_json
from thirtyx.contracts import SCHEMA_NAMES, load_schema, validate_instance
from thirtyx.decision import decide_experiment
from thirtyx.learning import append_record


class SchemaTests(unittest.TestCase):
    def test_contract_schemas_are_valid(self):
        for name in SCHEMA_NAMES:
            Draft202012Validator.check_schema(load_schema(name))

    def test_campaign_spec(self):
        validate_instance(demo_json("campaign.json"), "campaign-spec.schema.json")

    def test_observation(self):
        validate_instance(demo_json("observation.json"), "experiment-observation.schema.json")

    def test_decision_record(self):
        decision = decide_experiment(demo_json("campaign.json"), demo_json("observation.json"))
        validate_instance(decision, "decision-record.schema.json")

    def test_approval_manifest(self):
        payload = demo_json("approved-payload.json")
        manifest = create_manifest(payload, "ci", payload["campaign_id"])
        validate_instance(manifest, "approval-manifest.schema.json")

    def test_learning_record(self):
        campaign = demo_json("campaign.json")
        observation = demo_json("observation.json")
        decision = decide_experiment(campaign, observation)
        with tempfile.TemporaryDirectory() as directory:
            record = append_record(Path(directory) / "ledger.jsonl", campaign, observation, decision)
        validate_instance(record, "learning-record.schema.json")


if __name__ == "__main__":
    unittest.main()
