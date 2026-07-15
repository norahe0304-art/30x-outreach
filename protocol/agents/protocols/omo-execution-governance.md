<!--
[INPUT]: Depends on OMO agent discipline, capability-boundary.schema.md permission modes, and run-state-ledger.protocol.md.
[OUTPUT]: Provides execution_gates and final_readback lifecycle for all roles.
[POS]: protocols execution governance consumed by workflows and roles.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# OMO Execution Governance

OMO governs how a role gets work done. It is not an Ads engine, Event engine, or runtime dependency.

## Execution Gates

```text
trigger
  -> self-check
  -> plan
  -> delegate
  -> gather evidence
  -> execute by permission
  -> QA
  -> Metis/Momus review gate
  -> final_readback
```

## Gate Contract

- `trigger`: classify whether the role should act.
- `self-check`: verify tenant, permissions, host, and available evidence.
- `plan`: define tasks, risks, required tools, and stop conditions.
- `delegate`: assign Explorer, Librarian, Metis, Momus, or domain subroles when useful.
- `gather evidence`: collect source-backed artifacts before conclusions.
- `execute by permission`: respect read/observe/dry_run/propose. `apply` is reserved until a future runtime security review exists.
- `QA`: verify output against evidence, role schema, and workflow contract.
- `review gate`: use Metis/Momus for contradiction and plan-gate review when risk is high.
- `final_readback`: summarize actions, evidence, decisions, blocked items, run-state ledger target, and post_run_delta.

## Evidence Gates

Every role and workflow must collect:

- request/brief evidence
- source evidence
- plan/proposal evidence
- typed approval evidence when risk requires it
- final_readback evidence
- failure evidence for blocked or aborted actions

Approval evidence must conform to `agents/protocols/approval-evidence.schema.md#ApprovalReceipt`. Source, proposal, readback, and failure evidence must conform to `agents/protocols/approval-evidence.schema.md#EvidenceArtifact`.

## Completion Rule

A role is not complete until it has final_readback, a run-state ledger target,
and a post_run_delta route.

V1 completion cannot claim live external mutation. If a workflow reaches a live-action request, completion means a proposal, approval packet, blocked reason, readback target, and post_run_delta route.
