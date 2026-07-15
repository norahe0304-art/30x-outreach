<!--
[INPUT]: Depends on agents/thirtyx-outreach.agent.md.
[OUTPUT]: Provides a runtime-neutral doorway to the mounted 30x Outreach Agent.
[POS]: consumer instance entrypoint; a doorway, not the agent core.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Entrypoint

This is a doorway into the 30x Outreach Agent. It carries the request to the
mounted agent contract at `agents/thirtyx-outreach.agent.md`; it does not own the work.

Which agent runtime opens this doorway — Codex, Claude Code, Hermes, browser
automation, local runtime, MCP-backed tools, or another execution surface — is
the user's choice. Whatever opens it must load the mounted agent contract first,
then the base role (in the pinned protocol), the tenant overlay, the selected
playbook workflow, and the run-state ledger, and must pass the approval/evidence
gates that live in the playbook.

```yaml
entrypoint:
  mounted_agent: agents/thirtyx-outreach.agent.md
  runtime: user_choice
  must_load_first: agents/thirtyx-outreach.agent.md
  state_ledger: agents/state
  must_not:
    - act as the reasoning core in place of the mounted agent contract
    - bypass approval or evidence gates
    - store tenant truth here
```
