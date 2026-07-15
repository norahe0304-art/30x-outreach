# state/
> L2 | 父级: /agents/AGENTS.md

Run-state ledger for the 30x Outreach Agent. This directory stores structured
readbacks, proactive reusable-learning verdicts, verified GEB deltas, and reviewed tenant memory pointers. It never
stores raw transcripts, credentials, OAuth tokens, raw CRM exports, or unbounded
logs.

成员清单
runs/: Per-run readback YAML records. Each record names playbook, runtime surface, evidence refs, approval state, actions, blocked items, changed files, reusable-learning verdict, and GEB route. L2 map: runs/AGENTS.md.
deltas/: Verified GEB delta YAML records promoted from readbacks. L2 map: deltas/AGENTS.md.
memory/: Reviewed tenant memory pointers and stable operating facts. L2 map: memory/AGENTS.md.
memory/tenant-memory.md: Human-readable tenant memory ledger; facts require evidence, owner, last_verified_at, and review_after.

边界
state/ is durable agent memory, not runtime cache. Runtime-specific diagnostics
may be referenced by path, but raw session logs and secrets stay out.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
