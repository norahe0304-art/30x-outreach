<!--
[INPUT]: Depends on agents/thirtyx-outreach.overlay.md and protocol/agents/protocols/run-state-ledger.protocol.md.
[OUTPUT]: Provides reviewed tenant memory pointers for the 30x Outreach Agent.
[POS]: consumer instance state ledger; stores stable 30x facts only after evidence-backed readback.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Tenant Memory

Stable 30x facts belong here only after readback and evidence review.
Use pointers, not dumps.

```yaml
tenant_memory_records: []
```

## Memory Rule

Each record must include:

- source_of_truth
- evidence_url_or_path
- owner
- last_verified_at
- review_after
- contradiction_check

Never store credentials, OAuth tokens, raw CRM exports, raw transcripts, or
unbounded logs.
