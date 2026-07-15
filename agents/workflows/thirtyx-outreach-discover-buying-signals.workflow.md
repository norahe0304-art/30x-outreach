<!--
[INPUT]: Depends on outreach-growth-operator evidence/lead surfaces, thirtyx-outreach overlay bindings, and the 30x signal-evidence contract.
[OUTPUT]: Provides the Discover Buying Signals workflow from project scope to a sourced account-level signal set and audience proposal.
[POS]: Agent Core workflow behind discover-buying-signals; read/propose only and never a scraping or provider-write license.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Discover Buying Signals Workflow

```yaml
workflow_contract:
  id: thirtyx-outreach-discover-buying-signals
  role: outreach-growth-operator
  overlay: thirtyx-outreach
  default_mode: propose

  task_graph:
    - step: load_project_signal_thesis
      mode: read
      capability_refs:
        - market_evidence_source
      outputs:
        - project goal, ICP, exclusions, offer, eligible event types, evidence window, and signal expiry rules
    - step: collect_public_account_events
      mode: read
      capability_refs:
        - market_evidence_source
      outputs:
        - sourced hiring, funding, leadership, product, partnership, technology, and market events
        - observation URL or path, observed_at, subject, and bounded verbatim evidence
    - step: triangulate_buying_relevance
      mode: observe
      capability_refs:
        - market_evidence_source
      outputs:
        - accepted signals with an explicit link to the project problem
        - rejected weak signals, contradictions, staleness, and missing proof
    - step: resolve_candidate_accounts
      mode: read
      capability_refs:
        - lead_source
      outputs:
        - candidate accounts matching the ICP and accepted signal set
        - source timestamp, query scope, and unresolved account identity conflicts
    - step: produce_signal_evidence_packet
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - normalized signal ids with observation, source, observed_at, subject, and verified true
        - proposed audience-account set with no unsupported personalization
    - step: readback_and_learning
      mode: propose
      capability_refs:
        - memory_patch
      outputs:
        - sources inspected, accepted and rejected signals, evidence gaps, and next action
        - reusable-learning verdict and GEB route

  apply_lab:
    enabled: false
    runtime_binding_id: ""
    max_risk_class_v1: reversible_low
    allowed_operations: []
    forbidden_operations:
      - provider writes or campaign mutation
      - bypassing access controls or provider terms
      - treating titles, firmographics, or generic praise as buying signals
      - fabricating a source, timestamp, observation, or verification state
      - storing raw private exports in Agent Core state
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt
      - exact scope
      - pre_apply EvidenceArtifact
      - rollback plan
      - post_apply readback EvidenceArtifact

  future_live_action_policy:
    default_state: blocked_by_runtime_review
    allowed_only_after:
      - a separate run-outreach-experiment workflow
      - runtime_security_review_id
      - active Agent Core ApprovalReceipt
      - matching 30x exact-payload approval manifest
      - explicit --execute intent

  evidence_packet:
    required:
      - project signal thesis and evidence window
      - URL or path and observed_at for every accepted signal
      - contradiction and staleness check
      - accepted and rejected signal reasons
      - candidate account source and query scope

  readback:
    include:
      - what was reviewed
      - accepted, rejected, stale, and unresolved signals
      - evidence used
      - run-state ledger path
      - reusable learning verdict: persisted, proposed, or no-op
      - GEB route target path when learning should be persisted
      - safety check confirming no credentials, OAuth tokens, raw exports, raw transcripts, or unreviewed tenant facts are being stored
      - learning route

  proactive_learning_gate:
    required: true
    runtime_must_say:
      - "No reusable learning found; no GEB writeback recommended."
      - "Reusable learning found; recommended route is {route} -> {target_path} because {reason}."
      - "Reusable learning persisted to {target_path}; evidence was {evidence_ref}."
    no_silent_success: true
    writeback_policy:
      may_write_without_extra_prompt_when:
        - user explicitly asked to persist verified learning
        - evidence and route target are named
        - write target is outside protocol/
        - content contains no secrets, raw exports, raw transcripts, or unreviewed tenant facts
      otherwise:
        - stop at recommendation and ask for confirmation before editing repo files

  semantic_delta:
    default_route: workflow_patch
    promotion_requires:
      - repeated evidence
      - owner
      - review_after
      - contradiction check
```

## Playbook Rule

Discovery produces an evidence packet, not a send list. Recipient verification,
campaign approval, and provider execution belong to the experiment playbook.
