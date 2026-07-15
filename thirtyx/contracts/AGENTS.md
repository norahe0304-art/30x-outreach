# thirtyx/contracts/
> L2 | 父级: ../AGENTS.md

成员清单

__init__.py: 从 wheel resources 加载并验证具名 JSON Schema。
campaign-spec.schema.json: 约束 evidence、sequence 与结构化预注册阈值。
audience-batch.schema.json: 约束 recipient email verification、可追溯 buying signal 与 campaign identity。
experiment-observation.schema.json: 约束聚合样本、指标、观测时间与 demo 标记。
decision-record.schema.json: 约束 COLLECT/SCALE/KILL/LEARN 的确定性输出。
approval-manifest.schema.json: 约束人工身份、时间、recipient count 与 exact-payload hash。
learning-record.schema.json: 约束去标识实验记忆与前后 SHA-256 chain。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
