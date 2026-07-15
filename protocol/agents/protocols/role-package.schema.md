<!--
[INPUT]: Depends on agent-roles-spec concepts, install-mount-lifecycle.protocol.md, capability-boundary.schema.md, approval-evidence.schema.md, OMO execution gates, and GEB semantic/structural delta.
[OUTPUT]: Provides the canonical role_package schema and minimum validation for all Adaptive Marketing Agent OS roles.
[POS]: protocols shared schema consumed by reference roles, consumer-owned roles, overlays, and workflows.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Role Package Schema

Role is a complete operating package, not a prompt and not a single skill. A role can call skills and expose playbooks; each playbook is backed by a workflow contract.

## Required Object

```yaml
role_package:
  identity:
    id: ""
    name: ""
    version: ""
    domain: ""
    layer: ""
  tenant_overlay: ""        # optional
  purpose: ""
  when_to_use: []
  inputs: {}
  outputs: []
  role_instructions: {}
  skills:
    recommended: []
    optional: []
  playbooks:
    available:
      - id: ""
        name: ""
        workflow_contract: ""
        description: ""
        skills_called: []
        approval_gate: ""
        tenant_overlay_required: true
  memory_scope:
    base_role_memory:
      allowed: []
      forbidden: []
  runtime_requirements:
    binding_owner: "tenant_overlay_or_workflow"
    abstract_surfaces: []
    concrete_bindings_forbidden:
      - provider account IDs
      - MCP server config
      - plugin install state
      - runtime or host binding
      - project secrets
  capability_manifest:
    boundary_schema: "agents/protocols/capability-boundary.schema.md"
    default_profile: "propose_only"
    apply_lab_owner: "workflow"
    surfaces: {}
  lifecycle:
    states: []
  evidence_contract:
    artifact_schema: "agents/protocols/approval-evidence.schema.md#EvidenceArtifact"
    required: []
    forbidden: []
  approval_policy:
    default_state: "not_requested"
    future_live_action_state: "blocked_by_runtime_review"
    receipt_schema: "agents/protocols/approval-evidence.schema.md#ApprovalReceipt"
    approval_required_for: []
    approval_packet_requires: []
  success_criteria: []
  non_goals: []
  learning_rules:
    routes: {}
    promotion_requires: []
  versioning:
    owner: ""
    review_gate: ""
    status: "draft"
    change_log: []
```

## Field Rules

- `identity` names the role and its domain.
- `tenant_overlay` is optional and only points to a tenant overlay in composed role packages.
- `role_instructions` describes role behavior, not tenant facts.
- `skills` names callable atomic actions or candidate actions. Skills are not playbooks.
- `playbooks.available` names the role's callable business tasks. Each playbook points at a workflow contract; the role does not inline the workflow graph.
- `memory_scope` separates durable memory from forbidden raw dumps.
- `runtime_requirements` names abstract surfaces only. It does not bind providers, MCP servers, plugins, accounts, or hosts.
- `runtime_requirements.abstract_surfaces` must match `capability_manifest.surfaces` keys.
- `capability_manifest` binds abstract role surfaces to shared capability profiles. It must not restate raw mode lists.
- `evidence_contract` must include source-backed artifacts and readback.
- `approval_policy` must require a typed human receipt for any future live action.
- `learning_rules.routes` must route deltas through GEB, and `learning_rules.promotion_requires` must state promotion gates.
- `versioning` must include owner, review gate, status, and change log.

## Domain Role Constraint

Domain roles may instantiate shared `evidence_contract`, `approval_policy`, `learning_rules`, `runtime_requirements`, and `capability_manifest`; they must not introduce new protocol fields, permission modes, approval states, or evidence semantics. New shared semantics require a protocol update first.

Current role packages may bind surfaces only to capability profiles. V1 `mode: apply` is allowed only in workflow `apply_lab` steps with runtime binding, security review, an active `ApprovalReceipt`, and readback evidence.

Role packages must not include concrete `tools`, `plugins`, `host_adapters`, legacy `capability_surface`, `mcp_boundary`, or `permissions` sections. Those sections duplicate the runtime binding or capability protocols and create drift.

Concrete provider names, MCP bindings, plugin projection, runtime or host binding, tenant accounts, and project secrets belong in tenant overlays or workflow runtime bindings, not in base roles.

Role is the reusable product unit. Tenant attachments bind real systems. Playbooks expose business tasks. Workflow contracts execute those playbooks. Skills are atomic actions called by the workflow.

## Minimum Validation

This contract is executed by a single source of truth, not by a copy pasted here.
Run it directly, or let the pre-commit hook run it for you:

```bash
python3 scripts/validate_roles.py
```

The validator (`scripts/validate_roles.py`) enforces, for every
`agents/roles/*.role.md` (the reference roles):

- all required fields present, and no `workflow_contract` inside a `role_package`;
- `playbooks.available` exists, is non-empty, and every entry has `id`, `name`, and `workflow_contract`;
- no concrete `tools`, `plugins`, `host_adapters`, or legacy `capability_surface`, `mcp_boundary`, `permissions` sections;
- `runtime_requirements.abstract_surfaces` is a non-empty list matching `capability_manifest.surfaces`;
- `learning_rules.routes` is a map and `learning_rules.promotion_requires` is a list;
- `capability_manifest.boundary_schema` points at `capability-boundary.schema.md`;
- each `capability_manifest.surfaces.*` uses only `profile`, and the profile is
  defined by `capability-boundary.schema.md`.

Changing the rules above means changing `scripts/validate_roles.py` and this
section together — the executable and the prose stay isomorphic.

## Schema-ization Trigger

The validators are hand-written `if` checks on purpose. At this scale that is the
right call: direct, readable, zero-dependency, offline-verifiable — virtues a
pure-spec protocol repo should not trade away lightly. Note also that the
**highest-value** checks are not schema-able at all: filesystem existence of
referenced files (`require_existing`) and the cross-file `mount playbooks ⊆ role
playbooks` invariant live outside any JSON/YAML schema and stay in Python
regardless. Schema would only declutter the cheap shape rules (required keys,
enums, const values, forbidden keys), while splitting one validator into two
layers and adding a runtime dependency.

Move the shape rules into a single machine-readable schema (the validator loads
it; the semantic + filesystem checks stay in Python) WHEN any of these triggers
fires — not before:

- a **third** role-schema variant appears (two hand-synced copies is fine; three
  is drift waiting to happen);
- `REQUIRED_FIELDS` / `ALLOWED_PROFILES` in `validate_roles.py` **drift** from
  this document — and this trigger is **self-firing**: `scripts/check_schema_sync.py`
  (run by pre-commit)审判s the constants against this doc's `role_package` keys
  and `capability-boundary.schema.md`'s `capability_profiles`, failing the commit
  on any drift, so the same-fact-in-two-places bug cannot rot silently;
- the shape rules **outgrow** a readable if-chain (roughly: a reviewer can no
  longer hold the rule set in their head).

When that day comes, the goal is **one** source of truth, not a fourth copy:
make the data schema canonical, have both this prose and the validator derive
from it, and keep only the semantic/filesystem invariants as code. Prefer a
zero-dependency data file over pulling in `jsonschema` / `pydantic` unless the
shape surface has grown enough to earn the dependency.
