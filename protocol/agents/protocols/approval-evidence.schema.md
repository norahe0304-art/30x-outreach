<!--
[INPUT]: Depends on capability-boundary.schema.md approval gates and OMO evidence collection.
[OUTPUT]: Provides ApprovalReceipt and EvidenceArtifact contracts for approval, evidence, readback, apply lab, and future live-action gates.
[POS]: protocols hard safety contract consumed by role packages, workflows, overlays, and future runtime adapters.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Approval and Evidence Schema

Approvals and evidence are data contracts, not prose. A role may prepare an approval packet in v1. A workflow may execute V1 apply lab only when runtime binding, typed approval, exact scope, pre-apply evidence, and post-apply readback are all present.

## ApprovalReceipt

```yaml
approval_receipt:
  id: ""
  status: "active"
  channel: "chat | portal | document | runtime | api"
  receipt_url_or_path: ""
  approver_identity:
    name: ""
    handle_or_email: ""
    source_system: ""
  approver_authority:
    tenant: ""
    role: ""
    authority_source: ""
  action:
    action_hash: ""
    summary: ""
    risk_class: ""
    irreversible: false
  exact_scope:
    tenant: ""
    provider: ""
    account_or_portal: ""
    objects: []
    operations: []
  timing:
    requested_at: ""
    approved_at: ""
    expires_at: ""
  evidence:
    pre_action_evidence_ids: []
    post_action_evidence_ids: []
  revocation:
    revoked_at: ""
    revoked_by: ""
    reason: ""
```

Allowed receipt `status` values:

- `active`
- `expired`
- `revoked`
- `superseded`

## EvidenceArtifact

```yaml
evidence_artifact:
  id: ""
  type: "brief | source_export | dashboard | crm_record | draft_asset | proposal | approval | apply_run | readback | failure"
  source:
    name: ""
    url_or_path: ""
    collected_at: ""
    collected_by: ""
  scope:
    tenant: ""
    provider: ""
    account_or_portal: ""
    object_ids: []
    time_window: ""
  integrity:
    checksum_or_hash: ""
    redaction_status: "raw | redacted | synthetic | public"
    retention: ""
  readback:
    summary: ""
    linked_post_run_delta: ""
```

## Approval State Enum

```yaml
approval_state:
  allowed:
    - not_requested
    - apply_lab_requires_approval
    - approval_ready
    - approved_for_apply_lab
    - approved_for_future_runtime
    - rejected
    - expired
    - revoked
    - blocked_by_runtime_review
```

## Contract Rules

- `action_hash` must hash the exact proposed action packet, not a vague sentence.
- `exact_scope` must bind tenant, provider, account or portal, objects, and operations.
- `expires_at` is required for approvals that could affect external systems.
- A revoked, expired, or superseded receipt cannot authorize action.
- V1 apply lab requires `runtime_security_review_id`, an active `ApprovalReceipt`, pre-apply `EvidenceArtifact`, and post-apply readback.
- V1 apply lab may only execute operations named by the workflow `apply_lab.allowed_operations`.
- A workflow task may use `mode: apply` only when the workflow declares `apply_lab.enabled: true` and the task sets `apply_lab: true`.
- Future non-lab live actions require a separate protocol update and security review.
