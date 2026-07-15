<!--
[INPUT]: Depends on role-package.schema.md, agent-onboarding.contract.md, capability-boundary.schema.md, approval-evidence.schema.md, run-state-ledger.protocol.md, and geb-semantic-delta.md.
[OUTPUT]: Provides a simple install role, attach tenant, run playbook, and detach tenant note for Adaptive Marketing Agent OS agents.
[POS]: protocols optional packaging guardrail; not a fourth business object.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Role Install / Tenant Attach Note

This is not a core layer. It is packaging sugar around the role-first model.

Users do three things:

- install a reusable `role`;
- attach a `tenant`;
- run a role `playbook`.

## Operational Units

```yaml
role_install:
  id: ""
  role_package: ""
  workflow_templates: []
  protocol_refs:
    - role-package.schema.md
    - capability-boundary.schema.md
    - approval-evidence.schema.md
    - omo-execution-governance.md
    - geb-semantic-delta.md
  validation_fixtures: []
  skill_refs: []
  excludes:
    - tenant truth
    - provider account IDs
    - runtime bindings
    - runtime or host binding
    - approval receipts
    - evidence archives
tenant_attachment:
  id: ""
  tenant: ""
  mounts_on: ""
  tenant_overlay: ""
  workflow_bindings: []
  runtime_bindings: []
  approval_surfaces: []
  evidence_roots: []
  learning_routes: []
  state_roots:
    - agents/state/runs
    - agents/state/deltas
    - agents/state/memory
  excludes:
    - shared protocol changes
    - base role behavior changes
    - global provider secrets
playbook_activation:
  id: ""
  playbook: ""
  workflow_contract: ""
  skills_allowed: []
  mounted_role: ""
  attached_tenant: ""
  default_mode: "propose"
mounted_agent:
  id: ""
  installable: true
  detachable: true
  adaptive: true
  role: ""
  tenant_attachment: ""
  playbooks: []
  runtime_refs: []
  entrypoint_refs: []
  state_refs:
    - agents/state/AGENTS.md
    - agents/state/runs
    - agents/state/deltas
    - agents/state/memory/tenant-memory.md
  does_not_install:
    - credentials
    - provider account secrets
    - live mutation permission
  detach_preserves:
    - base role
    - workflow contracts
    - audit evidence
    - run readbacks
    - approved learning deltas
```

## Lifecycle

```text
install_role
  -> attach_tenant
  -> mount_agent
  -> activate_playbook
  -> dry_run_boot
  -> run
  -> write_run_readback
  -> route_geb_delta
  -> detach_tenant_when_needed
```

## Rules

- Role install is harmless: no tenant truth, no provider account, no runtime or host binding, no mutation permission.
- Tenant attach is reversible: detach removes project-private bindings without modifying the base role.
- Mounted agent install is composition only: it adds references and routing, not credentials or live mutation permission.
- Mounted agent detach removes tenant runtime projection, not the reusable role, playbooks, audit evidence, or approved learnings.
- Run-state ledger is durable tenant memory, not runtime cache. Detach may revoke live access, but must preserve or explicitly export required readbacks and approved deltas.
- Adaptive behavior is post-run: GEB may patch tenant memory, playbook workflow tails, skill candidates, or protocol proposals after readback.
- Provider runtime may be shared, but the tenant attachment decides which tenant and role may use it.
- `apply` is never installed by a role. It can only be enabled by a workflow-scoped `apply_lab`.
- Evidence and approval receipts are audit artifacts. Detach may remove live runtime access, but must not silently delete required audit evidence.
- GEB updates the right target after lifecycle changes: role, tenant attachment, playbook workflow, skill candidate, protocol, or AGENTS.md.

## Why This Stays Simple

The user-facing model has one product unit:

- Role: who the agent is, what skills it can call, what playbooks it can run, and which tenants can attach.

Tenant attachment and playbooks are part of operating the role. Capability, evidence, approval, OMO, and GEB are guardrails, not separate install layers.

## Removal Safety

Before detach or removal, the runtime must produce a readback:

```yaml
removal_readback:
  target: ""
  active_workflows: []
  runtime_bindings_revoked: []
  entrypoints_unprojected: []
  evidence_archives_retained: []
  run_readbacks_retained_or_exported: []
  verified_deltas_retained_or_exported: []
  tenant_memory_retained_or_exported: []
  blocked_reason: ""
```

If active `apply_lab` runs, pending approval receipts, or unresolved evidence handoffs exist, removal must stop and produce `blocked_reason`.
