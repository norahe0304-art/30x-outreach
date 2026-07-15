# thirtyx/learning/
> L2 | 父级: ../AGENTS.md

成员清单

__init__.py: 暴露 append/load/verify/head learning ledger API。
ledger.py: 用 SHA-256 hash chain 追加、验证并暴露去标识实验决策 head。

learning 只保存聚合实验事实，不保存联系人 PII；链内变更会破坏 hash，外部固定 head 可检测整链重写。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
