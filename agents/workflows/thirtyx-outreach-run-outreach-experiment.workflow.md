<!--
[INPUT]: Depends on outreach-growth-operator role surfaces, thirtyx-outreach overlay bindings, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides the evidence-to-approval workflow for a preview-first 30x outbound experiment.
[POS]: consumer instance workflow contract behind the role's run-outreach-experiment playbook.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Run Outreach Experiment Workflow

Machine-readable contract behind the `run-outreach-experiment` playbook. References role and
overlay by id, so it is path-portable across repos.

```yaml
workflow_contract:
  id: thirtyx-outreach-run-outreach-experiment
  role: outreach-growth-operator
  overlay: thirtyx-outreach
  default_mode: propose

  task_graph:
    - step: load_signal_backed_project_scope
      mode: read
      capability_refs:
        - market_evidence_source
        - outreach_experiment_engine
      outputs:
        - project goal, ICP, exclusions, offer, approved evidence roots, and candidate signals
        - explicit gaps that block audience construction or personalization
    - step: source_candidate_contacts
      mode: read
      capability_refs:
        - lead_source
      outputs:
        - candidate contacts scoped to the approved ICP and account set
        - source timestamp and provider query scope
    - step: verify_email_and_recipient_class
      mode: read
      capability_refs:
        - email_verification_source
      outputs:
        - valid email verification with provider and checked_at
        - non-free and non-role classification for every retained recipient
    - step: build_audience_and_campaign_contracts
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - audience batch binding each recipient to sourced, verified signal evidence
        - campaign spec with hypothesis, one changed variable, primary metric, guardrails, minimum sample, and frozen thresholds
    - step: run_quality_and_execution_preflight
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - deterministic ten-lens evaluation
        - verified audience preflight bound to campaign and sequence identity
        - blocked reason when evidence, verification, identity, or safety gates fail
    - step: prepare_exact_payload_approval
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - exact provider payload and recipient set for human review
        - 30x SHA-256 approval command and Agent Core ApprovalReceipt scope
        - rollback or irreversible-action note
    - step: preview_provider_execution
      mode: propose
      capability_refs:
        - outreach_experiment_engine
      outputs:
        - preview output proving no provider write occurred
        - exact future execute command, provider, campaign, recipient count, and required gates
    - step: readback_and_learning
      mode: propose
      capability_refs:
        - memory_patch
      outputs:
        - run readback with proposed, applied, and blocked actions
        - reusable-learning verdict and GEB route

  apply_lab:
    enabled: false
    runtime_binding_id: ""
    max_risk_class_v1: reversible_low
    allowed_operations: []
    forbidden_operations:
      - provider upload, campaign mutation, activation, or send from this propose-only workflow
      - execution without a verified signal-backed audience batch
      - execution without both an active Agent Core ApprovalReceipt and matching 30x exact-payload manifest
      - execution after any approved payload or recipient mutation
      - recipient identity in Agent Core state or the experiment ledger
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
      - runtime_security_review_id
      - active Agent Core ApprovalReceipt with exact tenant, provider, campaign, objects, and operations
      - matching 30x exact-payload approval manifest
      - verified signal-backed audience batch matching the approved recipients
      - explicit --execute intent naming the provider operation
      - pre-change evidence
      - rollback note
      - post-apply readback

  evidence_packet:
    required:
      - project brief, ICP, exclusions, and approved evidence roots
      - sourced and timestamped signal for every retained recipient
      - provider email verification for every retained recipient
      - campaign and audience contracts with matching campaign and sequence identity
      - deterministic evaluation and audience preflight output
      - exact provider payload, recipient count, and 30x approval manifest when execution is requested
      - preview output proving no external write occurred by default

  readback:
    include:
      - what was reviewed
      - what was proposed or applied
      - evidence used
      - campaign, sequence, provider, and recipient-count scope
      - quality, audience, approval, and execution-gate results
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
        - write target is an owning agent artifact, workflow, state ledger record, or protocol proposal outside protocol/
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

This is a role playbook, not a skill. It calls `30x-outreach` for deterministic
execution logic and stops at a provider preview. A future live run must satisfy
both Agent Core scope approval and the stronger 30x exact-payload gate.
