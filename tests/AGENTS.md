# tests/
> L2 | 父级: ../AGENTS.md

成员清单

test_approval_gate.py: 验证 hash 稳定性、payload 篡改阻断与 campaign 绑定。
test_sequence_linter.py: 验证合格 demo、无证据个性化硬阻断与 terminal control-character 清理。
test_sender_safety.py: 验证默认 preview 不写 history、缺失 manifest 无法 execute。
test_schemas.py: 验证 wheel 内置六份 JSON Schema 与 package demo/core 输出同构。
test_audience.py: 验证 verified + signal-backed audience、campaign 绑定与 recipient 去重。
test_observation.py: 验证 Instantly aggregate rate mapping、identity 绑定与 ledger 写入。
test_lead_pipeline_safety.py: 验证默认 staging 不上传、无 verification 或 signal 无法 execute。
test_decision.py: 验证四态决策、小样本安全 KILL、5%/10% bounce 硬边界、identity 绑定与 learning ledger 防篡改链。
test_pipeline.py: 验证 provider-neutral 去重、audience-gated execute 与 runnable plugin registry。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
