<!--
[INPUT]: 依赖 campaign experiment contract、aggregate observation 与 deliverability safety policy
[OUTPUT]: 对外提供预注册指标、bounce 硬边界与 SCALE/KILL/LEARN 决策协议
[POS]: references 的实验决策方法真相源；被 SKILL.md 与 deterministic engine 共同消费
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->
# Preregistered outreach experiments

Every campaign wave begins with a decision, not a dashboard. Record what will change, what should happen, and what result would alter the next production cycle before execution.

## Experiment contract

```json
{
  "hypothesis": "A specific claim about audience, message, and expected behavior",
  "variable": "The one major element changed in this wave",
  "primary_metric": "positive_reply_rate",
  "guardrails": ["bounce_rate < 0.02", "unsubscribe_rate < 0.01"],
  "minimum_sample_size": 100,
  "decision_thresholds": {
    "scale": "positive_reply_rate >= 0.03 and all guardrails pass",
    "kill": "positive_reply_rate < 0.01 after minimum sample",
    "learn": "otherwise isolate the weakest assumption and design the next wave"
  }
}
```

## Metric hierarchy

1. Primary outcome: positive replies, qualified meetings, or sourced pipeline—choose one.
2. Diagnostic metrics: delivery, bounce, total replies, CTA acceptance.
3. Guardrails: complaints, unsubscribes, domain health, and exclusion violations.
4. Context: segment, source, sequence version, offer, and send window.

Open rate is diagnostic at best. It must never be the sole SCALE decision because privacy protections and automatic image loading distort it.

## Bounce safety boundary

Campaign guardrails may be stricter, but they may never relax these system ceilings:

- `< 2%`: healthy operating target; continue to monitor sender and list quality.
- `2% to < 5%`: elevated risk; the preregistered campaign guardrail decides whether to KILL.
- `>= 5%`: absolute `KILL`; stop the campaign and audit verification before resuming.
- `>= 10%`: emergency stop; pause all sending and complete a sender/list audit.

The absolute ceilings apply before minimum sample size and cannot be overridden by a campaign spec. The 2% target, 5% review boundary, and 10% pause boundary follow the [Amazon SES enforcement guidance](https://docs.aws.amazon.com/ses/latest/dg/faqs-enforcement.html); operators remain responsible for the stricter rules of their actual provider.

## Learning record

After the minimum sample, append a result object containing observed metrics, decision, confidence limits when available, unexpected signals, and one proposed change. Never rewrite the original hypothesis or thresholds after seeing results.

## Decision vocabulary

- `SCALE`: preserve the winning variable and expand volume or an adjacent segment.
- `KILL`: stop the current variant; do not rationalize a failed preregistered threshold.
- `LEARN`: evidence is inconclusive or mixed; change one major assumption in the next wave.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
