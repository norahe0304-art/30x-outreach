# 30x Outreach Engine
> 独立发布仓库（从内部 monorepo 抽取，无外部父级 CLAUDE.md）

Claude Code Skill: 端到端冷邮件 outbound 引擎。
从业务画像到 ICP 定义，从 lead 获取到邮件创作，从专家评审到发送。
基于 Eric Siu 的 ai-marketing-skills/outbound-engine 改造，目标是世界顶级开源 outreach 系统。

## 成员清单

```
SKILL.md:               主操作手册，三层 skill 结构（frontmatter + body + 支撑文件）
CLAUDE.md:               本文件，L2 模块地图
config.example.json:     统一配置模板（API keys、发送限制、竞对列表）
requirements.txt:        Python 依赖

references/:             知识库（按领域拆分，Layer 3 按需加载）
  copy-rules.md:         邮件写作硬约束（开头、长度、CTA、链接、语气）
  expert-panel.md:       10 人专家评审团名单 + 评分维度
  instantly-rules.md:    Instantly 平台规则（变量、warmup、deliverability）
  icp-template.md:       ICP 数据收集模板 + Apollo 参数映射

scripts/:                Python 执行层（脚本自带 docstring，零 token 待机）
  config_loader.py:      统一配置加载器 + 输出格式化，被所有脚本依赖
  instantly-audit.py:    Instantly v2 API 审计（账号、campaign、warmup）
  lead-pipeline.py:      Apollo→LeadMagic→Instantly lead 全流程
  competitive-monitor.py:竞情追踪（定价快照 diff + 博客 + 招聘信号）
  cross-signal-detector.py: 跨源信号交叉检测（公司名/行业/关键词重叠）
  cold-outbound-sender.py:  审批后邮件发送（PII 安全扫描 + 日限控制）

data/:                   持久化数据层（30x 新增，Eric 原版无此结构）
  business/              业务画像（全局，只需配置一次）
    profile.example.json 业务画像 JSON schema 示例
  icps/                  多 ICP 目录（每个 ICP 独立子目录）
    profile.example.json ICP 画像 JSON schema 示例
  leads/                 Lead 数据（按 ICP 分目录：raw/verified/uploaded）
  intel/                 情报数据
    competitive/         竞情快照和报告
    signals/             跨信号检测结果
  output/                统一格式输出（所有脚本写入此目录）
```

## 数据流

```
config.json ─────────────────────────────────────────┐
                                                      │
domain → [自动扒 + 采访] → data/business/profile.json │
                                                      │
/30x-outreach {icp} ──┐                              │
                       ▼                              ▼
              data/icps/{icp}/profile.json ──→ lead-pipeline.py
                       │                              │
                       │                    data/leads/{icp}/*.json
                       │                              │
              competitive-monitor.py ──→ data/intel/competitive/
              cross-signal-detector.py → data/intel/signals/
                       │
                       ▼
              [邮件创作 + 10 专家评审 → 递归到 90+]
                       │
                       ▼
              [人工审核门 ⛔]
                       │
              user: "approved"
                       │
                       ▼
              cold-outbound-sender.py → data/output/send-log.json
```

## 架构决策

- **Creative Layer (AI) + Execution Layer (Python)**: AI 做判断/写作，Python 做 API 调用/数据处理
- **config.json 统一配置**: 所有 API key 和参数集中管理，不散落在 .env
- **统一 JSON 输出格式**: 每个脚本输出 `{module, timestamp, icp, status, data, summary}`
- **多 ICP 持久化**: `data/icps/{name}/profile.json`，支持 `$0` 变量切换
- **人工审核门**: Step 7 必须等 "approved" 才能发送，绝不自动发邮件

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
