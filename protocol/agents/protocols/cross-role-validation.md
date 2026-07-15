<!--
[INPUT]: Depends on role-package.schema.md, agent-onboarding.contract.md, and the reference roles in agents/roles/.
[OUTPUT]: Provides cross-role validation proving shared schema vs domain-specific runtime binding differences.
[POS]: protocols validation layer for proving the Agent OS is not Ads-only.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Cross-Role Validation

The shared protocol must be shaped so future domain roles can join without changing the core every time. The Ads and Event reference roles prove two distinct domains conform to one schema; they are optional seeds, not the canon of domains. A consumer may use them, fork them, or define its own role — the schema is the only invariant.

## Shared Schema

Both `ads-adaptive-operator` and `event-adaptive-operator` role packages must include these shared protocol fields:

- identity
- runtime_requirements
- capability_manifest
- approval_policy
- evidence_contract
- playbooks
- learning_rules

Role outputs may include `post_run_delta` as a promised deliverable. Role files declare available playbooks, but workflow files, not role files, define the concrete workflow graph and readback step that produces `post_run_delta`.

## Domain-Specific Runtime Bindings

`ads-adaptive-operator` declares abstract Ads surfaces such as `paid_media_platform`, `analytics_source`, `crm_quality_source`, and `landing_page_source`.

`event-adaptive-operator` declares abstract Event surfaces such as `event_asset_system`, `crm_context_source`, `document_source`, and `calendar_source`.

Tenant overlays map those abstract surfaces to concrete providers chosen by the consumer repo.

## Runtime Neutrality

Base roles and tenant overlays stay runtime-neutral. Which agent runtime runs a playbook (Codex, Claude Code, Hermes, browser automation, local runtime, MCP-backed tools, or another) is the user's choice and is never a protocol member. A tenant overlay may name a collaboration surface where humans approve and read back, but never a runtime.

## Seed Proofs

- The `ads-adaptive-operator` reference role proves the Ads domain conforms to the schema.
- The `event-adaptive-operator` reference role proves a second, different domain conforms to the same schema.
- Real consumer instances living in their own pinned repos are the live proof that the protocol grows runnable agents across domains.

## Validation Command

```bash
python3 - <<'PY'
from pathlib import Path
import re
import yaml

bad = [
    "required_for_" + "apply" + r"(?!_lab)",
    "blocked_until_" + "approval",
    r"post[_-]launch[_-]delta",
    "owner_" + "layer",
    "blocked_" + "modes",
]
hits = []
for path in Path("agents").rglob("*.md"):
    text = path.read_text()
    for pattern in bad:
        if re.search(pattern, text):
            hits.append((str(path), pattern))
if hits:
    raise SystemExit(hits)

allowed_workflow_modes = {"read", "observe", "dry_run", "propose", "apply"}
allowed_profiles = {
    "read_observe",
    "read_observe_propose",
    "propose_only",
    "paid_media_apply_lab_candidate",
    "draft_asset_apply_lab_candidate",
}
profile_rules = {
    "read_observe": {"modes": {"read", "observe"}, "apply_lab_candidate": False},
    "read_observe_propose": {"modes": {"read", "observe", "propose"}, "apply_lab_candidate": False},
    "propose_only": {"modes": {"propose"}, "apply_lab_candidate": False},
    "paid_media_apply_lab_candidate": {"modes": {"read", "observe", "dry_run", "propose"}, "apply_lab_candidate": True},
    "draft_asset_apply_lab_candidate": {"modes": {"read", "observe", "dry_run", "propose"}, "apply_lab_candidate": True},
}
role_required = [
    "identity", "purpose", "when_to_use", "inputs", "outputs",
    "role_instructions", "skills", "playbooks", "memory_scope",
    "runtime_requirements", "capability_manifest",
    "approval_policy", "evidence_contract", "learning_rules", "lifecycle",
    "success_criteria", "non_goals", "versioning",
]

def yaml_block(path):
    text = Path(path).read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise SystemExit(f"missing yaml block: {path}")
    return yaml.safe_load(match.group(1))

role_packages = {}

for path in Path("agents/roles").glob("*.role.md"):
    doc = yaml_block(path)
    pkg = doc.get("role_package")
    if not isinstance(pkg, dict):
        raise SystemExit(f"missing role_package: {path}")
    missing = [key for key in role_required if key not in pkg]
    if missing:
        raise SystemExit(f"missing {missing}: {path}")
    if "workflow_contract" in pkg:
        raise SystemExit(f"role_package must not include workflow_contract: {path}")
    playbooks = pkg.get("playbooks", {}).get("available")
    if not isinstance(playbooks, list) or not playbooks:
        raise SystemExit(f"playbooks.available must be non-empty: {path}")
    for playbook in playbooks:
        for key in ["id", "name", "workflow_contract"]:
            if key not in playbook:
                raise SystemExit(f"playbook entries require {key}: {path}")
    for forbidden in ["tools", "plugins", "host_adapters", "capability_surface", "mcp_boundary", "permissions"]:
        if forbidden in pkg:
            raise SystemExit(f"concrete runtime or duplicated capability field {forbidden}: {path}")
    runtime = pkg["runtime_requirements"]
    if runtime.get("binding_owner") != "tenant_overlay_or_workflow":
        raise SystemExit(f"bad runtime binding owner: {path}")
    abstract_surfaces = runtime.get("abstract_surfaces")
    if not isinstance(abstract_surfaces, list) or not abstract_surfaces:
        raise SystemExit(f"bad runtime_requirements.abstract_surfaces: {path}")
    if not isinstance(pkg["learning_rules"].get("routes"), dict):
        raise SystemExit(f"bad learning_rules.routes: {path}")
    if not isinstance(pkg["learning_rules"].get("promotion_requires"), list):
        raise SystemExit(f"bad learning_rules.promotion_requires: {path}")
    manifest = pkg["capability_manifest"]
    if manifest.get("boundary_schema") != "agents/protocols/capability-boundary.schema.md":
        raise SystemExit(f"bad capability boundary schema: {path}")
    if manifest.get("apply_lab_owner") != "workflow":
        raise SystemExit(f"bad apply_lab_owner: {path}")
    if set(abstract_surfaces) != set(manifest.get("surfaces", {})):
        raise SystemExit(f"runtime requirements and capability manifest drift: {path}")
    for surface, spec in manifest.get("surfaces", {}).items():
        if set(spec) != {"profile"}:
            raise SystemExit(f"surface must only contain profile in {surface}: {path}")
        if spec["profile"] not in allowed_profiles:
            raise SystemExit(f"unknown profile {spec['profile']} in {surface}: {path}")
    if path.parent.name == "roles":
        role_packages[pkg["identity"]["id"]] = pkg

for path in Path("agents/overlays").glob("*.overlay.md"):
    overlay = yaml_block(path).get("tenant_overlay")
    for key in ["identity", "runtime_bindings", "tenant_memory_records", "overlay_memory_rule"]:
        if key not in overlay:
            raise SystemExit(f"missing {key}: {path}")

for path in Path("agents/workflows").glob("*.workflow.md"):
    workflow = yaml_block(path).get("workflow_contract")
    for key in ["role", "overlay", "task_graph", "evidence_packet", "readback", "future_live_action_policy", "apply_lab"]:
        if key not in workflow:
            raise SystemExit(f"missing {key}: {path}")
    apply_lab = workflow.get("apply_lab") or {}
    role = role_packages.get(workflow.get("role"))
    if role is None:
        raise SystemExit(f"workflow references unknown role {workflow.get('role')}: {path}")
    role_surfaces = role["capability_manifest"]["surfaces"]
    for step in workflow.get("task_graph", []):
        mode = step.get("mode")
        if mode not in allowed_workflow_modes:
            raise SystemExit(f"bad workflow mode {mode}: {path}")
        refs = step.get("capability_refs")
        if not isinstance(refs, list) or not refs:
            raise SystemExit(f"workflow step missing capability_refs in {step.get('step')}: {path}")
        for ref in refs:
            if ref not in role_surfaces:
                raise SystemExit(f"workflow step references unknown capability {ref}: {path}")
            profile = role_surfaces[ref]["profile"]
            rule = profile_rules[profile]
            if mode == "apply":
                if step.get("apply_lab") is not True or not rule["apply_lab_candidate"]:
                    raise SystemExit(f"apply mode not allowed for capability {ref}: {path}")
            elif mode not in rule["modes"]:
                raise SystemExit(f"mode {mode} not allowed for capability {ref}: {path}")
        if mode == "apply":
            if not apply_lab.get("enabled"):
                raise SystemExit(f"apply step without enabled apply_lab: {path}")
            if step.get("apply_lab") is not True:
                raise SystemExit(f"apply step missing apply_lab true: {path}")
            for key in ["runtime_binding_id", "allowed_operations", "required_gates"]:
                if key not in apply_lab:
                    raise SystemExit(f"apply_lab missing {key}: {path}")
PY
```
