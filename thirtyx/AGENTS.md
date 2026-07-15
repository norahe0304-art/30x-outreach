# thirtyx/
> L2 | 父级: ../AGENTS.md

成员清单

__init__.py: 暴露 package version。
__main__.py: 支持 `python -m thirtyx` 的最小入口。
cli.py: `30x` 子命令路由，不承载业务规则。
evaluation.py: 十维确定性 sequence 评估与硬阻断。
approval.py: canonical JSON、SHA-256 manifest 与篡改验证。
decision.py: 用结构化阈值计算 COLLECT/SCALE/KILL/LEARN。
pipeline.py: provider-neutral 的 source→verify→dedupe→stage orchestration。
contracts/: wheel 内置 JSON Schema 与运行时 contract validation。
demo/: wheel 内置、无密钥的完整演示数据。
providers/: source、verifier、destination 插件契约与发现机制。
rendering/: 终端和 HTML proof artifact 渲染。
learning/: 去标识、可验证 hash chain 的实验决策记忆。

依赖方向

`demo → evaluation + decision → rendering → cli`

`providers → pipeline`，`decision → learning`；核心层不得依赖具体 SaaS provider。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
