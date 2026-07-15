<!--
[INPUT]: 依赖 root AGENTS.md 的安全不变量、pyproject 与 CI 命令
[OUTPUT]: 对外提供可复现开发环境、贡献范围与验收清单
[POS]: .github 的贡献入口；所有 PR 必须遵守 preview-first 与 GEB 同构
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Contributing

Thank you for helping make outbound more evidence-based, reviewable, and safe.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
30x demo --no-color
python -m unittest discover -s tests -v
```

## Good first contributions

- Add a quality-gate test for a real failure mode.
- Improve accessibility or clarity of the HTML proof artifact.
- Implement an offline provider with contract tests.
- Tighten a JSON Schema without breaking valid demo data.
- Clarify a measurement rule with an executable example.

## Non-negotiable safety rules

- Preview is the default. External writes require explicit execution.
- No real contact data, credentials, or live campaign output enters a fixture.
- Personalization requires a verified source and observation.
- Approval must bind the exact payload, not a mutable campaign name.
- Model output cannot override evidence, approval, thresholds, or execution gates.
- Learning records contain aggregate experiment data, never recipient PII.

## Pull requests

Keep one behavior change per PR. Add or update a regression test. Run the full offline suite. If a file, interface, module, or dependency changes, update its L3 header and the nearest `AGENTS.md` so the map remains aligned with the code.

Explain the user-visible outcome, the risk boundary, and the proof that no default external write was introduced.
