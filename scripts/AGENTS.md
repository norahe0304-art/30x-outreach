# scripts/
> L2 | 父级: ../AGENTS.md

成员清单

config_loader.py: 加载非敏感配置、环境变量凭据与统一输出封装。
instantly-audit.py: 只读审计 Instantly 账号、campaign、warmup 与容量。
lead-pipeline.py: Apollo sourcing → LeadMagic verification → Instantly dedupe；上传需显式执行。
competitive-monitor.py: 采集竞品定价与内容差异，并生成招聘信号检索提示。
cross-signal-detector.py: 跨数据源聚合公司、行业与关键词信号。
cold-outbound-sender.py: 验证审批 manifest、限额与内容后执行邮件发送。
sequence_linter.py: `thirtyx.evaluation` 的兼容入口，不复制核心规则。
approval/: `thirtyx.approval` 的兼容入口，不复制 hash 逻辑。

依赖边界

- API 客户端可依赖 `config_loader.py`，不得静默定义 fallback stub。
- `cold-outbound-sender.py` 必须依赖 `thirtyx.approval` 才能进入 live 路径。
- 核心评估、决策与审批只存在于 package；scripts 不能形成第二套真相。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
