# memory/
> L2 | 父级: /agents/state/AGENTS.md

Reviewed tenant memory pointers and stable operating facts for the 30x Outreach Agent
agent. Memory here is durable agent state, not runtime cache.

成员清单
tenant-memory.md: Human-readable tenant memory ledger; every fact needs evidence, owner, last_verified_at, and review_after.

边界
memory/ stores reviewed facts and pointers only. Literal secrets, raw CRM exports,
raw transcripts, and unreviewed tenant claims are forbidden.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
