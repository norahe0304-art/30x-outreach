# scripts/
> L2 | 父级: /protocol/AGENTS.md

Vendored validators and dry-run readiness tools for this consumer repo. These
tools judge the local mounted agent against the pinned protocol.

成员清单
validate_roles.py: Role package contract validator.
validate_mounted_agents.py: Mounted agent assembly validator; checks role, overlay, workflow, substrate, entrypoint, run-state, and proactive learning gate.
dry_run_agent.py: Runtime warm-up check; reads mounted agent, role, overlay, workflow, and state ledger without calling external systems.
check_run_conformance.py: Run readback conformance checker; judges structured run records against behavior gates.

边界
scripts/ validates and simulates. It does not connect to providers, mutate
business systems, or store credentials.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
