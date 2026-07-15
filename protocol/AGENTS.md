# protocol/
> L2 | 父级: /AGENTS.md

Pinned Adaptive Marketing Agent OS copy for this consumer repo. The pin is
recorded in VERSION; protocol semantics are read-only here and upgraded only by
re-pin.

成员清单
VERSION: Pin manifest. Names adaptive-marketing-agent-os, version, source commit, and vendored-copy resync rule.
agents/: Vendored protocol contracts and reference role library. L2 map: agents/AGENTS.md.
scripts/: Vendored validators and dry-run readiness tools. L2 map: scripts/AGENTS.md.

边界
protocol/ is the stable OS contract. Consumer-specific role edits, 30x
tenant truth, run readbacks, and memory live under ../agents/, not here.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
