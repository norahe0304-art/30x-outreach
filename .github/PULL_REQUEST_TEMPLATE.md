<!--
[INPUT]: 依赖 CONTRIBUTING.md、安全不变量、测试与 GEB 文档回环
[OUTPUT]: 对外提供 PR 结果、验证、风险与文档同步检查单
[POS]: .github 的变更质量门；让 reviewer 先看到结果与安全证据
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
## Outcome

What user-visible behavior changed?

## Proof

- [ ] `30x demo --no-color`
- [ ] `python -m unittest discover -s tests -v`
- [ ] New or changed behavior has a regression test

## Safety

- [ ] Preview remains the default
- [ ] No credentials, PII, or live results are included
- [ ] Approval and decision boundaries remain deterministic

## Map ↔ terrain

- [ ] L3 INPUT/OUTPUT/POS header matches the file
- [ ] Nearest `AGENTS.md` matches members and interfaces
- [ ] Root `AGENTS.md` changed if architecture changed
