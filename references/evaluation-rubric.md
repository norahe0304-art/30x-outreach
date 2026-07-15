# Ten-lens sequence evaluation

The evaluator is a transparent review framework, not a claim that ten independent human experts or ten independent models reviewed the work. Deterministic checks run through `30x evaluate`; optional model feedback must be labeled separately.

## 1. Targeting context

- The audience is narrow enough to share a buyer problem.
- Anti-ICP exclusions are explicit.
- The offer matches the audience's likely authority and timing.

## 2. Subject line

- Three to seven words.
- No shouting, emoji, or exclamation marks.
- Sounds like a relevant internal note, not a promotion.

## 3. Opening

- Does not begin with I, we, or our.
- Establishes relevance before introducing the sender.
- First touch stays below 80 words.

## 4. Relevance and evidence

- Every personalized claim points to a recorded evidence object.
- Evidence includes a source and `verified: true`.
- Job title and company alone are targeting context, not personalization evidence.

## 5. Value proposition

- Names one buyer problem and one plausible outcome.
- Avoids feature inventories and abstract claims.
- Gives the reader a reason to care now.

## 6. Proof integrity

- No fabricated familiarity, praise, clients, metrics, or intent.
- Placeholders are resolved before approval.
- Proof is attributable and used within its actual scope.

## 7. CTA

- One low-friction next action per touch.
- The ask matches the reader's likely stage of awareness.
- Early touches do not force a meeting.

## 8. Sequence logic

- Each touch adds a new angle, proof point, or useful artifact.
- Days are unique and increasing.
- The breakup closes the loop without guilt or false urgency.

## 9. Deliverability and compliance

- No URL in the first touch.
- Each touch remains under 120 words.
- Sending limits, suppression lists, and applicable legal requirements are respected.

## 10. Measurement and learning

- Hypothesis, primary metric, guardrails, and minimum sample are set before launch.
- SCALE, KILL, and LEARN conditions are explicit.
- Results become a versioned input to the next campaign wave.

## Decision boundary

The deterministic evaluator marks a sequence `READY_FOR_HUMAN_REVIEW` only when it scores at least 85/100 and has no hard blockers. That status is not permission to send. A human must review the exact payload and create an immutable approval manifest.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
