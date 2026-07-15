# protocols/
> L2 | 父级: /agents/AGENTS.md

成员清单
role-package.schema.md: Role guardrail，定义 base role 的 identity、instructions、abstract surfaces、memory、evidence、approval、learning。
capability-boundary.schema.md: Capability guardrail，定义 playbook workflow step 的 mode 与 capability_refs，不作为独立安装层。
approval-evidence.schema.md: Approval/evidence guardrail，定义 ApprovalReceipt、EvidenceArtifact 与 apply_lab 证据硬契约。
omo-execution-governance.md: OMO execution guardrail，定义 trigger/self-check/plan/delegate/evidence/QA/review/readback。
geb-semantic-delta.md: GEB learning guardrail，定义 persisted/proposed/no-op 主动学习判断、role、tenant attachment、playbook workflow、skill candidate 与 L1/L2/L3 的 post-run delta 回写。
run-state-ledger.protocol.md: Run-state guardrail，定义 consumer repo 的 structured readbacks、主动学习判断、verified GEB deltas、tenant memory pointers 与禁止 raw transcript/secret 的边界。
agent-onboarding.contract.md: Role-first onboarding，定义 role、tenant attachments、playbooks 的接入模型。
protocol-consumption.contract.md: Consumption guardrail，定义外部 repo 如何 pin、引用、校验本协议以长出自己的 agent;tenant 实例不住协议 repo。
agent-generation.loop.md: Generation loop，把 onboarding 变成可执行回路:scenario → scaffold → 生成 → 校验 → 跑 → GEB 学习;协议长出 agent，runtime 用户选。
install-mount-lifecycle.protocol.md: Packaging note，定义 install role、attach tenant、run playbook、detach tenant 的最小拆卸语义。
cross-role-validation.md: Validation guardrail，证明 Ads/Event 共用 role-first 模型且 playbook 不越权。

边界
protocols/ defines internal guardrails only. User-facing design remains one role that can attach tenants and run playbooks. Domain-specific facts belong in roles/, overlays/, workflows/, and consumer run-state ledgers.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
