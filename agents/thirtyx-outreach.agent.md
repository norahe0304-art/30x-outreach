<!--
[INPUT]: Depends on agents/outreach-growth-operator.role.md, agents/thirtyx-outreach.overlay.md, agents/workflows/thirtyx-outreach-run-outreach-experiment.workflow.md, agents/state/AGENTS.md, and the pinned protocol.
[OUTPUT]: Provides the mounted 30x Outreach Agent composition with three playbooks, runtime boundaries, and GEB readback routing.
[POS]: Agent Core consumer instance; orchestrates the 30x skill without duplicating its executable evidence, approval, or decision gates.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Agent

Mounted consumer instance of the Adaptive Marketing Agent OS. It composes the
pinned base role with the 30x tenant attachment and its playbooks. Runtime
(Codex / Claude Code / Hermes / browser / local / MCP-backed) is the user's
choice and is not durable agent state.

```yaml
mounted_agent:
  identity:
    id: thirtyx-outreach-agent
    name: 30x Outreach Agent
    version: 0.1.0
    domain: Outreach Growth
    tenant: 30x
    status: active_v1

  product_contract:
    user_facing_model: "install role, attach tenant, run playbook"
    role: agents/outreach-growth-operator.role.md
    tenant_attachment: agents/thirtyx-outreach.overlay.md
    work_substrate: .
    entrypoints:
      - agents/thirtyx-outreach.entrypoint.md

  adaptivity_contract:
    adaptive: true
    rule: "Every playbook run ends with readback plus a proactive reusable-learning verdict."
    updates_allowed:
      - tenant memory record
      - playbook workflow tail
      - readback shape
      - skill candidate
      - protocol proposal
    updates_forbidden:
      - silent base role mutation
      - hidden prompt drift
      - unbounded transcript storage
      - live mutation permission expansion without protocol review
    promotion_requires:
      - evidence_url_or_path
      - owner
      - last_verified_at
      - review_after
      - contradiction_check

  install_contract:
    installable: true
    unit: mounted_agent
    installs:
      - mounted agent definition
      - base role reference
      - tenant attachment reference
      - playbook workflow references
      - entrypoint reference
      - run-state ledger references
    does_not_install:
      - credentials
      - provider account secrets
      - live mutation permission
      - raw CRM export
      - unbounded tenant history
    install_check:
      - role file exists
      - tenant attachment file exists
      - playbook workflow files exist
      - entrypoint exists
      - run-state ledger exists
      - work substrate exists

  detach_contract:
    detachable: true
    detaches:
      - tenant runtime binding
      - entrypoint projection
    preserves:
      - base role
      - workflow contracts
      - required audit evidence
      - run readbacks
      - approved learning deltas
    removal_readback_required:
      - active workflows
      - runtime bindings revoked
      - entrypoint projections removed
      - evidence archives retained
      - run readbacks retained or exported
      - tenant memory retained or exported
      - blocked reason
    blocked_when:
      - active apply_lab run
      - pending approval receipt
      - unresolved evidence handoff

  boot_sequence:
    always_read:
      - agents/thirtyx-outreach.agent.md
      - agents/outreach-growth-operator.role.md
      - agents/thirtyx-outreach.overlay.md
      - agents/state/AGENTS.md
    select_playbook_by_intent:
      discover-buying-signals:
        workflow: agents/workflows/thirtyx-outreach-discover-buying-signals.workflow.md
      run-outreach-experiment:
        workflow: agents/workflows/thirtyx-outreach-run-outreach-experiment.workflow.md
      observe-and-generate-next-wave:
        workflow: agents/workflows/thirtyx-outreach-observe-and-generate-next-wave.workflow.md

  run_state_contract:
    root: agents/state
    run_readbacks: agents/state/runs
    geb_deltas: agents/state/deltas
    tenant_memory: agents/state/memory/tenant-memory.md
    protocol: protocol/agents/protocols/run-state-ledger.protocol.md
    forbidden_storage:
      - raw transcripts
      - credentials
      - OAuth tokens
      - raw CRM exports
      - unbounded runtime logs

  playbooks:
    discover-buying-signals:
      name: Discover Buying Signals
      workflow_contract: agents/workflows/thirtyx-outreach-discover-buying-signals.workflow.md
      default_mode: propose
      approval_required_before:
        - reading a non-public tenant system not already approved for bounded read access
        - enabling a new connector or provider binding
      readback_required:
        - sources and time windows inspected
        - accepted and rejected signals with evidence reasons
        - candidate accounts and unresolved evidence gaps
        - reusable learning verdict
        - proposed or persisted GEB route with target path
        - GEB learning route
    run-outreach-experiment:
      name: Run Outreach Experiment
      workflow_contract: agents/workflows/thirtyx-outreach-run-outreach-experiment.workflow.md
      default_mode: propose
      approval_required_before:
        - any provider upload, campaign mutation, activation, or send
        - any execution using --execute
        - any payload or recipient-set change after exact-payload approval
      readback_required:
        - campaign and sequence identity
        - audience verification and signal-evidence coverage
        - deterministic quality and preflight results
        - exact-payload approval manifest or explicit blocked reason
        - preview or approved execution evidence
        - reusable learning verdict
        - proposed or persisted GEB route with target path
        - GEB learning route
    observe-and-generate-next-wave:
      name: Observe and Generate Next Wave
      workflow_contract: agents/workflows/thirtyx-outreach-observe-and-generate-next-wave.workflow.md
      default_mode: propose
      approval_required_before:
        - reading non-public provider analytics outside an approved read binding
        - promoting experiment-specific facts into tenant memory
        - executing the generated next wave
      readback_required:
        - aggregate analytics source and campaign identity
        - normalized observation and deterministic decision
        - hash-chain record or explicit reason it was not appended
        - next-wave brief with one changed variable and evidence lineage
        - reusable learning verdict
        - proposed or persisted GEB route with target path
        - GEB learning route

  runtime_boundaries:
    tenant_id: thirtyx-outreach
    default_mode: propose
    read_allowed_without_approval:
      - AGENTS.md, SKILL.md, README.md, docs, references, package contracts, and fictional demo fixtures
      - public company pages, public hiring pages, public product releases, and cited public news
      - bounded aggregate provider exports already supplied for the active project
      - prior campaign, observation, decision, and ledger artifacts that contain no recipient identity
    apply_never_allowed_without:
      - active ApprovalReceipt
      - runtime_security_review_id
      - exact scope
      - pre-apply evidence
      - verified signal-backed audience batch
      - 30x exact-payload approval manifest matching the recipient set
      - explicit --execute intent naming the provider and operation
      - rollback note
      - post-apply readback
    forbidden_storage:
      - credentials
      - OAuth tokens
      - raw CRM exports
      - unbounded chat transcripts

  geb_learning:
    default_post_run_route: workflow_patch
    proactive_readback_required: true
    proactive_readback_rule: "Every run must say whether reusable learning exists, even when no repo write is performed."
    runtime_must_report:
      - reusable_learning_verdict: "persisted | proposed | no-op"
      - route: "tenant_memory_patch | workflow_patch | skill_candidate | protocol_update | no-op"
      - target_path
      - reason
      - safety_check: "no credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed tenant facts"
    persist_without_extra_prompt_only_when:
      - the user explicitly asked to persist verified learning
      - the delta is evidence-backed and scoped to the route target
      - the target is outside protocol/
      - the change contains no secrets or raw exports
    otherwise:
      - propose the target path and ask for confirmation before writing
    route_rules:
      tenant_memory_patch: stable tenant truth or source pointer
      workflow_patch: repeated playbook step, gate, failure behavior, tail rule, or readback change
      skill_candidate: repeated atomic action worth packaging
      protocol_update: shared OS constraint requiring cross-role proof
    required_fields:
      - evidence_url_or_path
      - owner
      - last_verified_at
      - review_after
      - contradiction_check
```

## Agent Rule

This mounted contract is runtime-neutral. Point any agent runtime at this file;
it reads the base role, tenant attachment, selected workflow, and run-state
ledger before calling `30x-outreach`. Agent Core owns orchestration and semantic
readback; the 30x package remains the source of truth for execution safety and
the aggregate experiment ledger.
