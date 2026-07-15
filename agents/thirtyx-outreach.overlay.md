<!--
[INPUT]: Depends on agents/outreach-growth-operator.role.md and 30x operating evidence.
[OUTPUT]: Provides 30x source pointers, provider bindings, approval surfaces, and memory boundaries for the Outreach Agent.
[POS]: Agent Core tenant attachment; binds the reusable role to the 30x repo without leaking provider credentials or project data.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach Overlay

Tenant truth for 30x, mounted on the `outreach-growth-operator` base role. Every fact
here must point to an evidence source and have a review path.

```yaml
tenant_overlay:
  identity:
    id: thirtyx-outreach
    tenant: 30x
    mounts_on: outreach-growth-operator
    version: 0.1.0

  tenant_truth_boundary:
    allowed_here:
      - stable operating contracts
      - source pointers
      - secret references only
      - approval owners or approval surfaces
    forbidden_here:
      - reusable base-role rules
      - shared Agent OS protocol
      - uncited tenant facts
      - credentials or provider secrets
      - literal secret values

  secret_reference_rule:
    allowed_reference_forms:
      - "${ENV_NAME}"
      - "vault://path/to/secret"
      - "1password://vault/item/field"
    forbidden:
      - API key values
      - OAuth tokens
      - passwords
      - private key material

  source_of_truth:
    runtime_repo:
      source_pointer: "."
      stable_meaning: "30x Outreach package, skill, contracts, tests, live adapters, documentation, and bounded local evidence."
    execution_skill:
      source_pointer: "SKILL.md"
      stable_meaning: "Atomic 30x execution protocol from ICP and verified signals through approval, preview, observation, and learning."
    package_engine:
      source_pointer: "thirtyx/ + thirtyx/contracts/"
      stable_meaning: "Deterministic audience, quality, approval, observation, decision, provider, rendering, and learning implementation."
    transitional_provider_adapters:
      source_pointer: "scripts/"
      stable_meaning: "Preview-first Apollo, LeadMagic, Instantly, and SMTP adapters pending full provider-package migration."
    experiment_memory:
      source_pointer: ".30x/learning.jsonl"
      stable_meaning: "Ignored local hash-chained campaign-level experiment ledger; contains aggregate evidence and no recipient identity."
    agent_memory:
      source_pointer: "agents/state/"
      stable_meaning: "Structured Agent Core run readbacks, reviewed semantic deltas, and stable tenant-memory pointers; never the experiment ledger."

  runtime_bindings:
    binding_owner: tenant_overlay
    abstract_surface_map:
      market_evidence_source:
        provider: runtime-approved public web and repository research
        mode: read_observe
      lead_source:
        provider: Apollo via scripts/lead-pipeline.py
        mode: read_observe
        secret_reference: "${APOLLO_API_KEY}"
      email_verification_source:
        provider: LeadMagic via scripts/lead-pipeline.py
        mode: read_observe
        secret_reference: "${LEADMAGIC_API_KEY}"
      outreach_experiment_engine:
        provider: 30x CLI and SKILL.md
        mode: read_observe_propose
      provider_analytics_source:
        provider: Instantly aggregate export via 30x observe-instantly
        mode: read_observe
        secret_reference: "${INSTANTLY_API_KEY}"
      memory_patch:
        provider: agents/state/memory/tenant-memory.md
        mode: propose

  approval_surfaces:
    chat_receipt:
      source_pointer: current runtime conversation
      stable_meaning: "Typed human approval for provider, account, campaign, operation, spend/risk, and exact scope."
    exact_payload_manifest:
      source_pointer: "30x approve PAYLOAD --by ID --campaign-id ID --output MANIFEST"
      stable_meaning: "SHA-256 manifest binding reviewer, campaign, payload, recipient count, and the exact approved content."
    repository_evidence:
      source_pointer: "campaign, audience, evaluation, observation, decision, and readback artifacts"
      stable_meaning: "Human-reviewable proof of what was proposed, validated, executed, observed, and learned."

  evidence_contract:
    artifact_schema: protocol/agents/protocols/approval-evidence.schema.md#EvidenceArtifact
    required:
      - source URL or export path
      - scope
      - time window
      - approval receipt for any future live action
      - final readback

  tenant_memory_records: []

  overlay_memory_rule:
    fields:
      - source_of_truth
      - evidence_url
      - owner
      - last_verified_at
      - review_after
      - promotion_target
      - expiry_reason
    promotion_targets:
      tenant_memory: "Stable 30x truth."
      workflow: "Repeated 30x procedure."
      skill_candidate: "Stable execution sequence worth packaging."
      protocol: "Shared OS change; requires cross-role proof."

  learning_route:
    default: tenant_memory
    must_not_promote_to_base_role:
      - provider account, campaign, workspace, or sender identifiers
      - provider subscription, quota, billing, or credential state
      - project ICP, recipient identity, raw leads, and private buying signals
      - campaign performance, sender health, and experiment-specific decisions
      - client positioning, exclusions, consent rules, and suppression data
```

## Overlay Rule

Durable cross-tenant rules must be proposed as GEB deltas, not silently copied
into the base role. Provider secrets remain environment references; live access
is not installed by this overlay and must be proven again for each project.
