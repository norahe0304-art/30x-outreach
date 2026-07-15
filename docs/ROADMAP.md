<!--
[INPUT]: 依赖当前 post-v0.2 package 能力、公开安全边界与尚未完成的 adapter 工作
[OUTPUT]: 对外提供按价值和稳定性排序的产品路线
[POS]: docs 的公开承诺边界；禁止把未完成能力写成现状
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Roadmap

## Unreleased — Evidence-gated live learning

- Require verified, non-free, non-role email evidence and a sourced buying signal for every executed recipient.
- Bind campaign identity to an exact audience batch before approval and external writes.
- Convert Instantly aggregates into deterministic observations and optional hash-chain records.
- KILL unsafe bounce or compliance guardrails before minimum sample completion.

## v0.2 — Executable proof

- Installable `30x` CLI and zero-credential offline demo.
- Structured campaign, observation, decision, approval, and learning contracts.
- Deterministic ten-lens gate and four-state decision engine.
- Exact-payload human approval and preview-first live scripts.
- Runnable provider entry points and a provider-neutral pipeline.
- Hash-chained aggregate learning ledger with an externally pinnable head.
- Self-contained HTML report, tests, CI, and release artifacts.

## v0.3 — Adapter ecosystem

- Promote Apollo, LeadMagic, and Instantly into isolated provider packages.
- Add reviewed CSV source/destination adapters for a fully local live path.
- Add suppression-list and consent hooks before any destination write.
- Add provider contract tests and recorded HTTP fixtures with no PII.
- Add CLI selection for source, verifier, and destination plugins.

## v0.4 — Experiment workspace

- Compare sequence versions and segments without changing frozen records.
- Generate a next-wave brief from verified prior decisions.
- Export redacted Markdown and HTML experiment timelines.
- Add optional model review with explicit provider, prompt, and provenance.

## v1.0 — Stable control plane

- Versioned public Python API and migration policy.
- Signed release provenance and reproducible packages.
- Pluggable policy gates for consent, jurisdiction, and platform rules.
- Reference deployments for local, CI, and team-operated workflows.

Requests are welcome as focused issues. The safety invariants in `AGENTS.md` are not roadmap tradeoffs.
