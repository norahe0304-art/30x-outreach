# agents/
> L2 | 父级: /AGENTS.md

This is the 30x Outreach **agent instance**, generated against the Adaptive
Marketing Agent OS protocol pinned under `../protocol/`. The protocol ships the
invariants (schema + gates + validators + run-state rails + GEB rails); this
directory holds the generated, tenant-specific composition for 30x.

成员清单
thirtyx-outreach.agent.md: Mounted agent. Composes the local consumer-owned `outreach-growth-operator` base role (agents/outreach-growth-operator.role.md) with the local overlay, playbooks, this repo as work substrate, a neutral entrypoint, and proactive GEB readback. Runtime is the user's choice.
thirtyx-outreach.overlay.md: 30x tenant attachment. Operating contracts, source pointers, runtime bindings, tenant memory records. mounts_on `outreach-growth-operator` by id.
thirtyx-outreach.entrypoint.md: Runtime-neutral doorway to the mounted agent.
outreach-growth-operator.role.md: Tenant-neutral Outreach Growth Operator role exposing signal discovery, experiment execution, and next-wave learning playbooks.
workflows/: Playbook workflow contracts. Reference role/overlay by id, require proactive reusable-learning verdicts, and stay path-portable. L2 map: workflows/AGENTS.md.
state/: Run-state ledger. Structured readbacks, proactive reusable-learning verdicts, verified GEB deltas, and reviewed tenant memory pointers; never raw transcripts or secrets. L2 map: state/AGENTS.md.

边界
This is a consumer instance, not the protocol. It never edits files under
`../protocol/`. Protocol-layer refs resolve to `protocol/agents/...`; instance
refs resolve here. Tenant truth, credentials, and live mutation permission never
go into the protocol copy. Secret references are allowed; literal secrets are not.

校验
python3 protocol/scripts/validate_mounted_agents.py --root . --glob 'agents/*.agent.md'
python3 protocol/scripts/dry_run_agent.py --root . --agent agents/thirtyx-outreach.agent.md --playbook discover-buying-signals
python3 protocol/scripts/dry_run_agent.py --root . --agent agents/thirtyx-outreach.agent.md --playbook run-outreach-experiment
python3 protocol/scripts/dry_run_agent.py --root . --agent agents/thirtyx-outreach.agent.md --playbook observe-and-generate-next-wave

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
