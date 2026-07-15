<!--
[INPUT]: Depends on role-package.schema.md for role_package fields.
[OUTPUT]: Provides embedded capability rules used by role playbook steps and role abstract surfaces.
[POS]: protocols safety guardrail consumed by roles and playbooks; not a separate user-facing layer.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Capability Guardrail

Capability is an internal guardrail embedded in the Role and its playbooks:

- Role declares abstract surfaces.
- Playbook steps reference those surfaces with `capability_refs`.
- Mode checks prevent a step from doing more than the surface allows.

## Runtime Split

- `provider-shared runtime`: external provider capability such as ads platforms, CRM, browser, docs, calendar, or memory.
- `project-private binding`: tenant/project scoped binding that limits account, tenant, object, and approval policy.
- `role-scoped manifest`: the role-specific list of abstract surfaces and capability profiles.

## Modes

| Mode | Meaning | Can change external state |
| --- | --- | --- |
| `read` | Read existing records or docs. | No |
| `observe` | Inspect live state without modifying it. | No |
| `dry_run` | Simulate an operation and produce expected result/risk. | No |
| `propose` | Produce a human-reviewable action plan. | No |
| `apply` | Execute an approved mutation through a workflow-scoped apply lab. | V1 apply lab only |

## Apply Gate

`apply` is not a default role permission. V1 may connect `apply` only inside a workflow-scoped `apply_lab`. Base roles still default to `propose`; a workflow must opt in before any task may use `mode: apply`.

Every V1 apply-lab mutation requires:

- `runtime_security_review_id`
- role-level risk class
- tenant/account binding
- named human approver
- typed approval receipt
- pre-apply evidence
- post-apply readback
- rollback plan or explicit irreversible-action acknowledgement

If any item is missing, execution must stop at `propose`.

## Internal Capability Record

```yaml
capability:
  provider: ""
  binding: ""
  scope: "tenant"
  modes: ["read", "observe", "dry_run", "propose", "apply"]
  default: "propose"
  max_mode_v1: "apply_lab"
  future_live_action_requires_approval: true
  allowed_operations: []
  approval_gate: ""
  evidence_readback: []
  rollback_or_dry_run: ""
```

## Internal Capability Profiles

Profiles are the single source of truth for mode semantics. Role packages bind
surfaces to profile names; they do not restate raw mode lists.

```yaml
capability_profiles:
  read_observe:
    modes: [read, observe]
    default: read
    apply_lab_candidate: false
  read_observe_propose:
    modes: [read, observe, propose]
    default: observe
    apply_lab_candidate: false
  propose_only:
    modes: [propose]
    default: propose
    apply_lab_candidate: false
  paid_media_apply_lab_candidate:
    modes: [read, observe, dry_run, propose]
    default: propose
    apply_lab_candidate: true
  draft_asset_apply_lab_candidate:
    modes: [read, observe, dry_run, propose]
    default: propose
    apply_lab_candidate: true
```

## Workflow Apply Lab Record

```yaml
apply_lab:
  enabled: false
  runtime_binding_id: ""
  max_risk_class_v1: "reversible_low"
  allowed_operations: []
  forbidden_operations: []
  required_gates:
    - runtime_security_review_id
    - active ApprovalReceipt
    - exact tenant/account/object scope
    - pre_apply EvidenceArtifact
    - rollback plan or irreversible-action acknowledgement
    - post_apply readback EvidenceArtifact
```

## Role Surface Binding Record

Role `capability_manifest.surfaces.*` entries may only use these fields:

- `profile`: required capability profile name from this protocol.

Base role surfaces must not list raw `modes`. Apply belongs to workflow
`apply_lab` records and task steps that explicitly set `apply_lab: true`.

No domain role may add extra capability surface keys without updating this shared protocol first.

## Workflow Step Binding

Workflow steps are where safety becomes execution. Every task graph step declares which role surfaces it uses.

```yaml
workflow_step:
  step: ""
  mode: "read"
  capability_refs: []
```

Rules:

- `capability_refs` must be non-empty for every workflow step.
- Every ref must exist in the mounted role's `capability_manifest.surfaces`.
- Step `mode` must be allowed by every referenced capability profile, except `apply` may only appear when `apply_lab: true` and the referenced profile is an `apply_lab_candidate`.
- Runtime bindings in the tenant overlay must map every referenced abstract surface before execution starts.
- If a step needs a surface not listed by the role, stop and propose a role or workflow patch through GEB.

## Unbound Surface Binding

A named abstract surface may have no reachable runtime connector in the current
runtime: the overlay maps the surface to a provider, but no connector is wired,
or the wired one is unreachable. Blocking apply on a missing binding is the safe
floor — but the agent must not stop at "I cannot," and must never silently
degrade to manual (such as asking the user to paste in what the connector would
have read). It proposes the binding:

- names the unbound surface and its overlay `binding_rule`;
- names the connector type that best fits the surface and the chosen runtime —
  MCP server, CLI, browser session, API binding, ... — with no default toward any
  one kind; which runtime, and which connector, stays the user's choice;
- gives the exact `runtime_bindings` entry it would add to the tenant overlay, as
  a reference only — secrets stay in env or a secret store, never in the overlay;
- requests authorization, then stays at `propose` until it is granted.

Proposing the binding is the generative half of the same rule that blocks apply
on a missing binding. The agent closes the gap it found instead of handing it
back.

## Example Runtime Bindings

Concrete runtime bindings may map abstract surfaces like this:

- `paid_media_platform` -> tenant-approved paid media provider.
- `event_asset_system` -> tenant-approved event page, email, workflow, list, or asset system.
- `crm_context_source` -> tenant-approved CRM, CDP, warehouse, or other read-scoped customer data source.
- `document_source` -> tenant-approved document surface.
- `memory_patch` -> tenant memory or skill candidate proposal path.

## Forbidden

- No global tool exposure.
- No provider config files in this protocol directory or base role package.
- No runtime- or host-specific behavior such as chat thread UX or a particular agent runtime.
