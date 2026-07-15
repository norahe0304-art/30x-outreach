# runs/
> L2 | 父级: /agents/state/AGENTS.md

Per-run readbacks for the 30x Outreach Agent agent. Runtime surfaces write structured
records here after real or dry-run executions; raw transcripts stay out.

成员清单
.gitkeep: Keeps the run readback directory present until the first `*.readback.yaml` exists.
2026-07-15-agent-core-integration.readback.yaml: Apply-mode readback for pinning Agent Core v0.3.10 and mounting the three-playbook 30x Outreach Agent.

边界
runs/ stores bounded readback records only: task outcome, evidence refs,
approval state, changed files, blocked items, and reusable-learning verdict.
No credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed facts.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
