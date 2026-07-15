<!--
[INPUT]: 依赖 git history 与 pyproject.toml package version
[OUTPUT]: 对外提供版本级新增、变更、安全修复与迁移信息
[POS]: docs 的用户可读变更记录；发布 tag 前必须更新
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Changelog

All notable changes are documented here. The project follows semantic versioning after `1.0.0`; `0.x` releases may refine schemas with explicit migration notes.

## Unreleased

### Added

- `audience-batch` contract requiring provider verification, timestamps, non-free/non-role emails, and at least one sourced buying signal per recipient.
- `30x preflight` to bind a quality-approved campaign to its exact execution audience.
- `30x observe-instantly` to convert aggregate provider analytics into an observation, deterministic decision, and optional learning-ledger record.
- Fictional audience and Instantly analytics fixtures covering the complete offline proof.

### Changed

- Provider destinations, the legacy Instantly uploader, and the SMTP sender now fail closed before external writes when audience proof is missing.
- Safety guardrail failures return `KILL` immediately, even before the preregistered minimum sample is reached.
- Bounce rate now has non-overridable system ceilings: `>=5%` returns absolute `KILL`; `>=10%` returns emergency-pause guidance for all sending.

### Security

- Approval alone no longer authorizes sending; the approved recipient set must exactly match a verified, signal-backed audience batch.

## 0.2.0 — 2026-07-14

### Added

- Installable `30x` CLI with demo, evaluation, decision, approval, provider, doctor, and learning commands.
- Offline fictional campaign producing a terminal report and self-contained HTML artifact.
- Structured JSON Schemas for campaigns, observations, decisions, approvals, and learning records.
- Wheel-packaged runtime contract validation shared by source and installed CLI paths.
- Deterministic `COLLECT`, `SCALE`, `KILL`, and `LEARN` engine.
- Runnable provider registry and provider-neutral pipeline.
- SHA-256 chained aggregate learning ledger.
- Offline safety regression suite across Python 3.9, 3.11, and 3.12.

### Changed

- Replaced string-based thresholds with machine-readable comparison rules.
- Moved authoritative evaluation and approval logic from scripts into the package.
- Reframed named “expert” simulation as ten transparent evaluation lenses.

### Security

- External writes remain preview-only until explicit execution.
- Live sends require an exact-payload approval manifest.
- History and learning artifacts exclude raw recipient identity.
- SMTP delivery uses a persisted pending→sent journal to prevent crash-driven duplicate sends.
- CLI output strips terminal control characters from campaign and plugin text.
