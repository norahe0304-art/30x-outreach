# agents/
> L2 | 父级: /protocol/AGENTS.md

Vendored protocol agent contracts for the 30x Outreach Agent consumer instance.
These files are pinned protocol inputs, not tenant truth.

成员清单
protocols/: Internal guardrails for role, playbook, workflow, approval/evidence, run-state, GEB learning, generation, and consumption.
roles/: Reference role library. Optional seeds only; consumer-owned roles live in ../../agents/.

边界
protocol/agents/ is read-only in this consumer repo. Re-pin the protocol to
upgrade; do not edit vendored contracts for local tenant behavior.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
