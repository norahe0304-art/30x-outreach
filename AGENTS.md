# 30x Outreach — 可审计的 outbound experiment control plane
Python 3.9+ + JSON Schema + requests + unittest

<directory>
thirtyx/ - 可安装 package：CLI、audience gate、评估、观测、决策、审批、provider、渲染与 learning ledger
scripts/ - 旧式 SaaS adapter 与兼容 CLI；所有外部写入默认关闭
docs/ - 架构、provider、roadmap 与 changelog
assets/ - README 与发布使用的真实离线 demo 视觉
references/ - ICP、文案、评估与实验方法
tests/ - 决策、schema、审批、pipeline 与发送安全的离线回归
.github/ - CI、release、依赖更新与社区协作配置
data/ - 本地业务、ICP、线索、情报与输出；真实数据不入库
</directory>

<config>
AGENTS.md - 项目宪法、依赖方向与不可破坏的安全边界
README.md - 对外产品入口、quickstart 与能力地图
SKILL.md - Agent 执行工作流与决策门
pyproject.toml - package、依赖、console script 与 wheel 配置
config.example.json - 非敏感 live adapter 参数模板
.env.example - 外部服务凭据名称模板
.gitignore - 隔离凭据、PII、ledger 与运行产物
LICENSE - MIT 许可证
</config>

## 不变量

- 外部写操作默认关闭；只有显式 `--execute` 才可上传或发送。
- 人工批准绑定 exact payload 的 SHA-256；批准后的修改必须失败关闭。
- 确定性规则、模型建议与人工判断分层记录，模型不得伪装成独立人类专家。
- 个性化只能引用带 source 的 verified observation；无证据时宁可留空。
- 凭据只从环境变量读取，不进入 CLI 参数、配置、报告或 ledger。
- 公共 demo 完全虚构并标记 `DEMO DATA`；联系人 PII 不进入仓库或 learning ledger。
- 实验在执行前冻结 hypothesis、primary metric、guardrails、sample 与 SCALE/KILL/LEARN 阈值。
- package 核心不得依赖具体 SaaS；外部 provider 通过 Protocol 与 entry point 接入。

## 依赖方向

`demo → evaluation + decision → rendering → cli`

`audience → pipeline + live execution`；`providers → pipeline`；`observation → decision → learning ledger`；`approval → live execution`

`references + thirtyx/contracts → thirtyx core → scripts adapters → ignored local outputs`

## 变更日志

- 2026-07-15: 新增 verified + signal-backed audience contract、全外部写入 preflight 与 Instantly aggregate → decision → ledger 闭环；安全 guardrail 可在小样本阶段立即 KILL。
- 2026-07-14: 建立可安装 `30x` CLI、结构化四态决策、provider contract、离线 HTML proof 与 hash-chain learning ledger。
- 2026-07-14: 引入十维确定性评估、预注册实验、不可变审批、默认 preview、隐私安全历史、schemas、tests 与 CI；移除人格模拟评审和明文凭据。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
