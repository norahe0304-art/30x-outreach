<!--
[INPUT]: Depends on AGENTS.md L1/L2 docs, role-package.schema.md learning_rules, run-state-ledger.protocol.md, and OMO final_readback.
[OUTPUT]: Provides proactive learning verdicts, post_run_delta routing, run-state delta records, knowledge_updates, skill_candidate_updates, and structural L1/L2/L3 sync rules.
[POS]: protocols GEB governance for semantic and structural evolution.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# GEB Semantic and Structural Delta

GEB is not only learning. Every result must decide both semantic placement and structural documentation impact.
The runtime must say that decision out loud before the run is considered complete.

## Delta Classes

- `tenant_memory_patch`: tenant-only operating truth or source pointer.
- `industry_playbook_patch`: reusable domain pattern across tenants.
- `role_schema_patch`: role package field or boundary change.
- `workflow_patch`: playbook execution graph, gate, failure behavior, or readback change.
- `skill_patch`: improvement to an atomic reusable action called by one or more playbooks.
- `new_skill_candidate`: candidate produced from repeated stable sessions.
- `protocol_update`: shared semantic change required by multiple roles.

## Structural Delta

Structural deltas preserve L1/L2/L3 isomorphism for every created, moved, renamed, or responsibility-shifted artifact.

- L1 `/AGENTS.md`: project constitution and global map.
- L2 `/{module}/AGENTS.md`: module map and member list.
- L3 file header: `[INPUT]`, `[OUTPUT]`, `[POS]`, `[PROTOCOL]`.

## Post Run Delta

```yaml
post_run_delta:
  run_readback_ref: "agents/state/runs/<run_id>.readback.yaml"
  reusable_learning_verdict: "persisted | proposed | no-op"
  semantic_delta:
    class: ""
    target: ""
    evidence_id: ""
    delta_record_ref: "agents/state/deltas/<delta_id>.yaml"
    persistence_state: "persisted | proposed | none"
    reason: ""
    safety_check: "no credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed tenant facts"
  structural_delta:
    files_created: []
    files_moved: []
    files_responsibility_changed: []
    agents_md_updates: []
  knowledge_updates: []
  skill_candidate_updates: []
  final_readback: ""
```

## Proactive Learning Verdict

Every runtime must end a real run with exactly one reusable-learning verdict:

- `persisted`: a verified reusable delta was written back to its owning artifact.
- `proposed`: a reusable delta appears valid, but needs owner confirmation before writing.
- `no-op`: no reusable learning should be persisted from this run.

For `persisted` and `proposed`, the readback must name the route, target path,
evidence reference, reason, and safety check. The safety check must explicitly
confirm that no credentials, OAuth tokens, raw exports, raw transcripts, or
unreviewed tenant facts are being stored.

The final readback is not the raw session transcript. It is a structured summary
that points to evidence, decisions, blocked items, and approved semantic deltas.
Stable learning becomes durable only after it is written as a reviewed
`geb_delta_record` in the run-state ledger or as a patch to the owning role,
overlay, workflow, skill candidate, protocol, or AGENTS.md file.

## Skill Candidate Rule

Interactive session learning is valid, but it becomes a skill candidate only after:

- repeated stable use
- evidence of replayability
- replay artifact with input fixtures, expected outputs, tool versions, and pass/fail criteria
- redaction review for tenant secrets, raw CRM exports, credentials, and private personal data
- reviewer approval
- documented GEB route

Record & Replay is useful for stable workflows, not every session.

## Replay Artifact

```yaml
replay_artifact:
  id: ""
  source_sessions: []
  redaction_status: ""
  tool_versions: []
  input_fixtures: []
  expected_outputs: []
  pass_fail_criteria: []
  reviewer: ""
  target_skill_candidate: ""
```

Session distillation may create memory, playbook/workflow, or skill-candidate deltas. If the whole business route changes, patch the playbook workflow. If an atomic reusable action stabilizes, promote or patch a skill. Only a replay artifact can promote a session pattern into a skill candidate.
