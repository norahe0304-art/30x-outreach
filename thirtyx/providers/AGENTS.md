# thirtyx/providers/
> L2 | 父级: ../AGENTS.md

成员清单

base.py: 定义 source、verifier、destination Protocol 与 provider metadata。
registry.py: 注册 provider metadata 或 runnable instance，并发现 `thirtyx.providers` entry points。
builtins.py: 描述 Apollo、LeadMagic、Instantly 与 SMTP 的能力和环境变量。

插件必须暴露 ProviderInfo；runnable instance 可由 registry.get() 注入 pipeline，是否写入仍由 `execute` gate 决定。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
