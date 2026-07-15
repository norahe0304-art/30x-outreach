---
name: 30x-outreach
description: Build auditable outbound experiments from ICP and verified signals through evidence-backed sequences, deterministic evaluation, immutable human approval, explicit execution, and SCALE/KILL/LEARN records. Use for cold outbound design, campaign optimization, demand experiments, ICP management, and safe execution.
argument-hint: <icp-name>
---

<!--
[INPUT]: 依赖 30x CLI、data profiles、references、schemas 与 preview-first live adapters
[OUTPUT]: 对外提供从 ICP 到 learning ledger 的 agent 执行协议
[POS]: repo 的 agent workflow；不得绕过 evidence、approval、threshold 或 execution gate
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# 30x Outreach

Operate outbound as a compounding learning system. Preserve the reasoning between signal, message, result, and next action instead of treating each campaign as disposable copy.

## Dynamic context

### Business profile
!`cat ${CLAUDE_SKILL_DIR}/data/business/profile.json 2>/dev/null || echo '{"status":"NOT_CONFIGURED","action":"Run Step 1"}'`

### Active ICP
!`cat ${CLAUDE_SKILL_DIR}/data/icps/$0/profile.json 2>/dev/null || echo '{"status":"NOT_FOUND","icp":"$0","action":"Run Step 2"}'`

### Latest competitive intelligence
!`cat ${CLAUDE_SKILL_DIR}/data/intel/competitive/latest.json 2>/dev/null || echo '{"status":"NO_DATA","action":"Run Step 4"}'`

### Latest cross-signals
!`cat ${CLAUDE_SKILL_DIR}/data/intel/signals/latest.json 2>/dev/null || echo '{"status":"NO_DATA","action":"Run Step 4"}'`

## Non-negotiable invariants

1. Never invent familiarity, praise, customer intent, proof, metrics, clients, or URLs.
2. A personalization claim requires an observation, source, and `verified: true` evidence object.
3. Keep deterministic checks separate from model-assisted qualitative review.
4. Default to preview. External writes require explicit `--execute` and prior human review.
5. Email execution additionally requires a manifest matching the exact payload hash.
6. Never pass secrets through CLI flags, config files, generated copy, or reports.
7. Never commit real PII or run artifacts.
8. Freeze hypothesis and decision thresholds before execution.

## Startup router

- No business profile: run Step 1.
- Business profile exists but `$0` ICP does not: run Step 2.
- ICP exists: identify whether the request concerns infrastructure, intelligence, sourcing, sequence design, approval, execution, or learning and enter the corresponding step.
- No ICP argument: list directories under `data/icps/` and ask which ICP to use or create.

## Step 1: Build the business profile

Collect two evidence streams in parallel.

From public sources:

- Homepage, product, pricing, about, case studies, documentation, and recent launches.
- Positioning, buyer, offer, price, proof, objections, and alternatives.
- Source URL and retrieval date for every claim used later.

From the operator:

1. What do you sell in one sentence?
2. Who buys it and who never should?
3. What next action is appropriate for a cold prospect?
4. Why do customers choose it over alternatives?
5. What proof can be disclosed and attributed?
6. What objection appears most often?

Flag contradictions instead of silently merging them. Save reviewed output to `data/business/profile.json` and a readable brief beside it.

## Step 2: Define ICP and anti-ICP

Use `references/icp-template.md`. Record:

- Primary, secondary, and excluded titles.
- Company size, vertical, geography, stage, and technical context.
- Buying signals and the source able to verify each signal.
- Anti-ICP company and contact traits.
- Buyer problem, offer fit, objections, and acceptable proof.
- Apollo parameters as a separate execution mapping.

Save structured data to `data/icps/{icp-name}/profile.json`. Confirm the profile before sourcing.

## Step 3: Audit infrastructure

Set `INSTANTLY_API_KEY` in the environment and run:

```bash
python3 scripts/instantly-audit.py
```

Report sending accounts, warmup state, campaign metrics, conservative capacity, and blockers. This step is read-only. If no account meets the configured readiness rules, stop before sourcing or execution.

## Step 4: Collect and connect signals

Run competitive intelligence and cross-source detection as relevant:

```bash
python3 scripts/competitive-monitor.py
python3 scripts/cross-signal-detector.py
```

Normalize useful observations into evidence objects:

```json
{
  "id": "signal-001",
  "observation": "A directly observable fact",
  "source": "https://source.example/item",
  "verified": true
}
```

Do not convert a weak keyword match into intent. Keep confidence and provenance visible.

## Step 5: Source, verify, and stage leads

Run the lead pipeline without `--execute` first:

```bash
python3 scripts/lead-pipeline.py \
  --icp {icp-name} \
  --campaign-id YOUR_CAMPAIGN_UUID
```

The pipeline reads Apollo, verifies through LeadMagic, deduplicates against Instantly and exclusions, and stores raw/verified/ready data locally. It does not upload in the default mode.

Review targeting parameters, counts, verification loss, exclusions, and the staged lead file. Only then may the operator authorize the same command with `--execute`.

## Step 6: Preregister the campaign

Create a campaign spec matching `thirtyx/contracts/campaign-spec.schema.json` with:

- Audience and anti-ICP.
- Buyer problem and value proposition.
- Verified evidence objects.
- Hypothesis and the single variable under test.
- Primary metric and guardrails.
- Minimum sample size.
- SCALE, KILL, and LEARN thresholds.
- Ordered steps with subject, body, CTA, and evidence IDs.

Use `references/measurement-framework.md` and `references/copy-rules.md`. Never choose thresholds after results arrive.

## Step 7: Run the quality gate

```bash
30x evaluate \
  data/campaign-spec.json \
  --output data/output/sequence-evaluation.json
```

The ten lenses are targeting context, subject line, opening, relevance/evidence, value proposition, proof integrity, CTA, sequence logic, deliverability/compliance, and measurement/learning.

`READY_FOR_HUMAN_REVIEW` requires at least 85/100 and zero hard blockers. It is not permission to execute. If model-assisted critique is used, label the model and prompt, preserve its output separately, and never present it as independent human expertise.

## Step 8: Bind human approval to the exact payload

First preview the exact payload:

```bash
python3 scripts/cold-outbound-sender.py \
  --approved-file data/cold-outbound-approved.json
```

Present the campaign, audience, recipient count, every message, evidence, evaluation, hypothesis, thresholds, limits, and planned execution path. Wait for explicit human approval of that exact file.

After approval, create the manifest:

```bash
30x approve data/cold-outbound-approved.json \
  --by REVIEWER_ID \
  --campaign-id CAMPAIGN_ID \
  --output data/campaign-approval.json
```

Do not modify the payload after this command. Any change must invalidate the approval and trigger a new review.

## Step 9: Execute explicitly

```bash
python3 scripts/cold-outbound-sender.py \
  --approved-file data/cold-outbound-approved.json \
  --approval-manifest data/campaign-approval.json \
  --execute
```

The sender must fail closed on manifest mismatch, missing credentials, suspicious content, duplicate recipients, or daily-limit exhaustion. It must never remove records from the approved payload.

## Step 10: Close the learning loop

Once the preregistered minimum sample is reached, write aggregate metrics matching `thirtyx/contracts/experiment-observation.schema.json`, then compute the decision from the frozen campaign:

```bash
30x decide \
  data/campaign-spec.json \
  data/experiment-observation.json \
  --output data/output/decision.json \
  --html data/output/decision.html

30x record \
  data/campaign-spec.json \
  data/experiment-observation.json \
  --ledger .30x/learning.jsonl

30x verify-ledger --ledger .30x/learning.jsonl
```

`COLLECT`, `SCALE`, `KILL`, and `LEARN` are computed, not narrated after the fact. Preserve the original campaign spec and aggregate observation. Feed the hash-chained record into the next brief as a versioned input, not retroactive justification. Keep recipient identity out of the ledger.

## Reference map

| File | Purpose |
|---|---|
| `references/icp-template.md` | ICP and anti-ICP collection |
| `references/copy-rules.md` | Copy hard constraints |
| `references/evaluation-rubric.md` | Ten transparent evaluation lenses |
| `references/measurement-framework.md` | Preregistration and decision semantics |
| `references/instantly-rules.md` | Platform variables and deliverability |
| `thirtyx/contracts/campaign-spec.schema.json` | Campaign contract |
| `thirtyx/contracts/approval-manifest.schema.json` | Approval contract |
| `thirtyx/contracts/experiment-observation.schema.json` | Aggregate observation contract |
| `thirtyx/contracts/decision-record.schema.json` | Deterministic decision contract |
| `thirtyx/contracts/learning-record.schema.json` | Hash-chain memory contract |

## Configuration

Use `config.json` only for non-secret settings. All credentials must come from environment variables named in `.env.example`.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
