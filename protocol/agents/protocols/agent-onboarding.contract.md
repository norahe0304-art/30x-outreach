<!--
[INPUT]: Depends on role-package.schema.md, capability-boundary.schema.md, approval-evidence.schema.md, run-state-ledger.protocol.md, and geb-semantic-delta.md.
[OUTPUT]: Provides the role-first onboarding contract for any new marketing agent.
[POS]: protocols scale rule for adding future Ads, Event, SEO, Content, Lifecycle, or Partner Ops agents.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Agent Onboarding Contract

New marketing agents must be boring to add. A new agent starts with one role. Tenants attach to that role. Playbooks are callable business tasks inside the role. Each playbook is backed by an internal workflow contract and may call reusable skills.

## Required Declaration

```yaml
agent_onboarding:
  domain: ""
  mounted_agent:
    file: ""
    installable: true
    detachable: true
    adaptive: true
  role:
    file: ""
    purpose: ""
    abstract_surfaces: []
    learning_routes: []
    tenant_attachments:
      - file: ""
        runtime_bindings: []
        approval_surfaces: []
        tenant_memory_rules: []
    playbooks:
      - file: ""
        workflow_contract: ""
        skills_called: []
        task_graph: []
        evidence_required: []
        approval_gate: ""
        readback: ""
  run_state:
    ledger_root: "agents/state"
    run_readbacks: "agents/state/runs"
    verified_deltas: "agents/state/deltas"
    tenant_memory: "agents/state/memory/tenant-memory.md"
```

## Naming

- `skill`: atomic reusable action, such as spend check, search-term clustering, landing-page relevance review, or CRM lead-quality lookup.
- `playbook`: business task route exposed by a role, such as daily maintenance, account review, event launch kit, or keyword expansion.
- `workflow_contract`: machine-readable execution graph behind a playbook. It owns steps, modes, capability refs, evidence, approval, failure behavior, and readback.

## Onboarding Steps

1. Declare `domain`: Ads, Event, SEO, Content, Lifecycle, Partner Ops, or another named marketing domain.
2. Declare `role`: who the agent is, what abstract surfaces it needs, where learning can land, which skills it can call, and which playbooks it can run.
3. Attach tenant: bind real systems, approval surfaces, and tenant memory rules.
4. Dry-run the mounted playbook: prove the runtime can parse role, overlay, workflow, and run-state ledger without side effects.
5. Run a playbook: task graph, capability refs, evidence, approval gate, and readback.
6. Route GEB delta: update tenant memory, workflow tail, playbook rule, skill candidate, or protocol proposal.

## Acceptance

- Base role contains no tenant truth.
- Overlay contains no unbounded transcript, CRM export, raw campaign history, or literal secret value.
- Secret references may point to `${ENV_NAME}`, `vault://...`, or `1password://...`; API keys, OAuth tokens, passwords, and private keys are never stored in markdown.
- Consumer repo contains `agents/state/` for structured readbacks, verified deltas, and reviewed tenant-memory pointers.
- Install surface stays simple: install role, attach tenant, run playbook.
- Base role does not restate raw capability modes; it references shared capability profiles through abstract surfaces.
- Base role does not bind concrete tools, plugins, MCP providers, accounts, or runtimes.
- Playbook stops at propose unless its workflow contract has scoped apply_lab, runtime binding, and full approval/evidence gates.
- Runtime and host choice are the user's, never a protocol member; the durable protocol surface is role + playbook + run-state ledger + GEB learning.
- Runtime adapter choice is replaceable execution surface; it may read and write approved state ledger artifacts but does not own durable memory.
- GEB route is a post-run guardrail backed by a structured readback.
- Mounted agent is installable, detachable, and adaptive without installing credentials or live mutation permission.
