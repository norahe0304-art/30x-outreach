"""
[INPUT]: 依赖 wheel 内置 JSON Schema、demo/core API 与 Agent Core role/overlay/workflow contracts
[OUTPUT]: 验证 30x 跨阶段 schema 及 mounted agent 的 playbook、capability、双审批与双记忆边界
[POS]: tests/ 的机器/语义双相契约回归测试
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""

import re
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from thirtyx.approval import create_manifest
from thirtyx.cli import demo_json
from thirtyx.contracts import SCHEMA_NAMES, load_schema, validate_instance
from thirtyx.decision import decide_experiment
from thirtyx.learning import append_record


ROOT = Path(__file__).resolve().parent.parent
PROFILE_MODES = {
    "read_observe": {"read", "observe"},
    "read_observe_propose": {"read", "observe", "propose"},
    "propose_only": {"propose"},
}


def markdown_yaml(path, key):
    match = re.search(r"```yaml\n(.*?)\n```", path.read_text(), re.S)
    if not match:
        raise AssertionError(f"missing YAML contract: {path}")
    return yaml.safe_load(match.group(1))[key]


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

    def test_agent_core_playbooks_bind_declared_capabilities(self):
        agent = markdown_yaml(ROOT / "agents/thirtyx-outreach.agent.md", "mounted_agent")
        role = markdown_yaml(ROOT / "agents/outreach-growth-operator.role.md", "role_package")
        overlay = markdown_yaml(ROOT / "agents/thirtyx-outreach.overlay.md", "tenant_overlay")
        role_playbooks = {item["id"] for item in role["playbooks"]["available"]}
        surfaces = role["capability_manifest"]["surfaces"]
        bindings = overlay["runtime_bindings"]["abstract_surface_map"]

        self.assertEqual(set(agent["playbooks"]), role_playbooks)
        self.assertEqual(set(surfaces), set(bindings))
        for playbook in agent["playbooks"].values():
            workflow = markdown_yaml(ROOT / playbook["workflow_contract"], "workflow_contract")
            self.assertEqual(workflow["role"], role["identity"]["id"])
            self.assertEqual(workflow["overlay"], overlay["identity"]["id"])
            for step in workflow["task_graph"]:
                for surface in step["capability_refs"]:
                    self.assertIn(surface, surfaces)
                    profile = surfaces[surface]["profile"]
                    self.assertIn(step["mode"], PROFILE_MODES[profile])

    def test_agent_core_live_execution_requires_both_approval_layers(self):
        agent = markdown_yaml(ROOT / "agents/thirtyx-outreach.agent.md", "mounted_agent")
        workflow = markdown_yaml(
            ROOT / "agents/workflows/thirtyx-outreach-run-outreach-experiment.workflow.md",
            "workflow_contract",
        )
        gates = " ".join(agent["runtime_boundaries"]["apply_never_allowed_without"])
        future_gates = " ".join(workflow["future_live_action_policy"]["allowed_only_after"])
        for phrase in ("Agent Core ApprovalReceipt", "30x exact-payload approval manifest", "--execute"):
            self.assertIn(phrase, f"{gates} {future_gates}")
        self.assertFalse(workflow["apply_lab"]["enabled"])

    def test_agent_core_keeps_semantic_and_experiment_memory_separate(self):
        agent = markdown_yaml(ROOT / "agents/thirtyx-outreach.agent.md", "mounted_agent")
        overlay = markdown_yaml(ROOT / "agents/thirtyx-outreach.overlay.md", "tenant_overlay")
        agent_memory = agent["run_state_contract"]["root"]
        experiment_memory = overlay["source_of_truth"]["experiment_memory"]["source_pointer"]
        self.assertEqual(agent_memory, "agents/state")
        self.assertEqual(experiment_memory, ".30x/learning.jsonl")
        self.assertNotEqual(agent_memory, experiment_memory)


if __name__ == "__main__":
    unittest.main()
