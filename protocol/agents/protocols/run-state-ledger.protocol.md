<!--
[INPUT]: Depends on geb-semantic-delta.md, approval-evidence.schema.md, omo-execution-governance.md, and protocol-consumption.contract.md.
[OUTPUT]: Provides the run-state ledger contract for readbacks, proactive learning verdicts, verified deltas, and tenant memory pointers in consumer repos.
[POS]: protocols runtime-state guardrail; keeps durable agent state versioned without storing raw sessions or secrets.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Run State Ledger Protocol

Runtime sessions are execution surfaces, not durable memory. A consumer repo may
persist only structured run state: readbacks, verified GEB deltas, and reviewed
tenant memory records.

## Directory Contract

Generated consumer instances use this minimal ledger:

```text
agents/state/
  AGENTS.md
  runs/
    <run_id>.readback.yaml
  deltas/
    <delta_id>.yaml
  memory/
    tenant-memory.md
```

The ledger is optional for a protocol-only repo and required for generated
consumer instances that want cross-runtime continuity.

## Run Readback

```yaml
run_readback:
  id: ""
  mounted_agent: ""
  playbook: ""
  runtime:
    name: ""
    version: ""
    surface: "codex | claude-code | browser-automation | internal-tool | local-runtime | other"
  mode: "read | observe | dry_run | propose | apply"
  started_at: ""
  completed_at: ""
  approval_state: ""
  evidence_refs: []
  actions:
    proposed: []
    applied: []
    blocked: []
  files_changed: []
  geb_delta:
    verdict: "persisted | proposed | no-op"
    class: ""
    target: ""
    path: ""
    evidence_ref: ""
    reason: ""
    safety_check: "no credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed tenant facts"
  final_readback: ""
  not_stored:
    - raw transcript
    - credentials
    - OAuth tokens
    - raw CRM export
    - unbounded logs
```

## GEB Delta Record

```yaml
geb_delta_record:
  id: ""
  class: "tenant_memory_patch | industry_playbook_patch | role_schema_patch | workflow_patch | skill_patch | new_skill_candidate | protocol_update"
  target: ""
  evidence_id: ""
  owner: ""
  last_verified_at: ""
  review_after: ""
  contradiction_check: ""
  changes: []
  promoted_to: ""
```

## Rules

- The ledger stores semantic run state, not raw chat history.
- Every persisted run record must include final readback and evidence refs.
- Every run record must include a reusable-learning verdict: `persisted`, `proposed`, or `no-op`.
- `persisted` and `proposed` verdicts must name route, target path, evidence ref, reason, and safety check.
- Every delta record must name a GEB class, target, owner, review date, and contradiction check.
- Secrets may appear only as references to approved secret stores or environment variables, never as literal values.
- Runtime metrics such as token usage are optional and must stay under `runtime.metrics`; they are diagnostic, not memory.
- Apply-mode records require an active `ApprovalReceipt` and post-apply readback.
- Protocol-level changes are proposed as `protocol_update`; consumer repos do not edit pinned `protocol/` directly.

## Conformance Replay

Structural validators prove a contract is well-formed; they cannot prove a run
behaved. The readback is the run's own declared record, so it can be judged after
the fact:

```bash
python3 protocol/scripts/check_run_conformance.py --root . --glob 'agents/state/runs/*.readback.yaml'
```

It fails the run if the readback violates an invariant no static check could
reach: an `applied` action without active approval, evidence, and a post-apply
readback (propose-first broken); a missing or incomplete reusable-learning
verdict (silent success); or a literal secret stored instead of a reference. This
moves behavioral compliance from "trust the runtime" to "the run's own record is
judged." Honest limit: it judges what the readback declares, not ground truth — a
lying readback can pass, so the replay complements, never replaces, the approval
and evidence gates.
