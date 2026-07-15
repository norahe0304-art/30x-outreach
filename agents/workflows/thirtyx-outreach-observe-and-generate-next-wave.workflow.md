<!--
[INPUT]: Depends on provider aggregate analytics, the 30x observation/decision/ledger engine, prior frozen campaign evidence, and Agent Core memory routing.
[OUTPUT]: Provides the Observe and Generate Next Wave workflow from aggregate results to a deterministic decision and evidence-linked next-wave brief.
[POS]: Agent Core learning workflow; keeps experiment truth in the 30x hash chain and semantic run state in Agent Core.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Observe and Generate Next Wave Workflow

```yaml
workflow_contract:
  id: thirtyx-outreach-observe-and-generate-next-wave
  role: outreach-growth-operator
  overlay: thirtyx-outreach
  default_mode: propose

  task_graph:
    - step: load_frozen_experiment_identity
      mode: read
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - campaign id, sequence version, hypothesis, variable, metric, guardrails, sample, and frozen thresholds
    - step: read_aggregate_provider_analytics
      mode: read
      capability_refs:
        - provider_analytics_source
      outputs:
        - campaign-level sent, delivered, bounced, replied, positive, and unsubscribed counts
        - analytics source, collection time, provider campaign identity, and data-window boundaries
    - step: normalize_experiment_observation
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - provider-neutral aggregate observation with matching campaign and sequence identity
        - explicit missing, inconsistent, or out-of-window metrics
    - step: compute_frozen_decision
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - exactly one COLLECT, SCALE, KILL, or LEARN state
        - failed guardrails, missing metrics, primary value, and deterministic reason
        - immediate 5 percent bounce KILL or 10 percent emergency-pause instruction when applicable
    - step: preserve_experiment_truth
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - proposed hash-chain append containing aggregate evidence only
        - current and expected ledger heads or explicit reason no record should be appended
    - step: generate_one_variable_next_wave_brief
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - decision and source-record references
        - winning variable to preserve or failed assumption to replace
        - one new hypothesis and one major changed variable
        - audience, evidence, channel, primary metric, guardrails, sample, and frozen decision criteria
        - unresolved questions that must remain questions rather than invented facts
    - step: route_semantic_learning
      mode: propose
      capability_refs:
        - memory_patch
      outputs:
        - Agent Core run readback pointing to the 30x ledger without copying aggregate or recipient data
        - reusable-learning verdict and evidence-backed GEB route

  apply_lab:
    enabled: false
    runtime_binding_id: ""
    max_risk_class_v1: reversible_low
    allowed_operations: []
    forbidden_operations:
      - provider mutation or next-wave execution
      - changing the frozen prior hypothesis or decision thresholds
      - storing recipient identity in either durable memory layer
      - copying raw provider exports into Agent Core state
      - promoting one experiment result into a reusable rule without repeated evidence
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
      - next-wave brief is materialized as a new frozen campaign and audience contract
      - separate run-outreach-experiment preflight
      - active Agent Core ApprovalReceipt
      - matching 30x exact-payload approval manifest
      - explicit --execute intent

  evidence_packet:
    required:
      - prior frozen campaign spec
      - aggregate provider analytics with campaign identity and time window
      - normalized observation and deterministic decision
      - 30x ledger head before and after any approved append
      - next-wave brief referencing the decision and source evidence

  readback:
    include:
      - what was reviewed
      - observation, decision, and proposed ledger action
      - next-wave hypothesis and the single changed variable
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

The 30x ledger owns aggregate experiment truth. Agent Core stores only the run
readback and a pointer to that truth; the next wave is a new frozen experiment,
never a rewrite of the prior record.
