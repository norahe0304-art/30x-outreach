# Cold Email Copy Rules

Rules for writing and evaluating cold email copy. Apply to every step in every sequence.

> [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

---

## First Sentence Rules

**NEVER start with:**
- "I" — e.g., "I came across your company..."
- "We" — e.g., "We help companies like yours..."
- "Our team" — e.g., "Our team specializes in..."
- "I wanted to" — e.g., "I wanted to reach out because..."
- "Hope this finds you well" or any version of it
- "My name is..." (save for follow-ups if needed, never Step 1)

**Start with one of:**
- **A verified company signal** — a cited hire, launch, filing, or published statement
- **A sourced market observation** — relevant to the segment, not disguised as one-to-one research
- **A specific finding** — linked to a recorded evidence object
- **A relevant trend** — with enough context for the reader to judge it

The first sentence earns the second. If it doesn't make the prospect think "hm, relevant," the email is dead.

---

## Body Length Rules

| Step | Max sentences | Notes |
|------|--------------|-------|
| Step 1 | 3 sentences | Open + value + CTA. That's it. |
| Steps 2-4 | 3-5 sentences | Add new angle or asset, not a repeat |
| Step 5 (bump) | 1-2 sentences | Short. "Still relevant?" style. |
| Step 6 (breakup) | 2-3 sentences | Leave value, don't close your file. |

If a step is longer than this, cut it. Ruthlessly.

---

## Stats and Social Proof

Use a number only when its source, scope, and permission are recorded. Calling a number an “observation” does not make an unsupported claim safe.

**Never fabricate:**
- Specific client names unless verified and approved
- Revenue numbers or % improvements unless you have the actual data
- Podcast episodes or content references unless they exist and are linkable
- Case study specifics — if you can't verify it, generalize it

---

## CTAs

**Soft asks (preferred):**
- "Worth a look?"
- "Want the data?"
- "Does this match what you're seeing?"
- "Relevant to what you're working on?"
- "Happy to share what we found — useful?"

**Hard asks (avoid in Step 1):**
- "Book a call with me" → too much commitment too early
- "Schedule 30 minutes" → presumes interest
- "Let's hop on a call" → pushy
- "Are you free Thursday?" → too forward for a stranger

Use hard asks only in Step 4+ if you've gotten engagement signals. Even then, soften them.

---

## Links

- **Step 1:** No links (deliverability + trust)
- **Steps 2-3:** Max 1 link, only if it adds genuine value (a case study, a report, a tool)
- **Breakup email:** Include 1 real link to genuinely useful content (not a sales page)
- **Never:** Hallucinate URLs. All links must be verified real pages before use.
- **Never:** Link to a landing page with a form in Steps 1-2 — it signals spray-and-pray

---

## Breakup Email (Final Step)

**Correct:**
> Leave something genuinely useful. A real article, a real report, a real piece of content that relates to their problem.
> "In case it's useful regardless — here's the framework we use: [real URL]. No pressure on the rest."

**Incorrect:**
> "Just wanted to close the loop / closing your file / marking you as not interested"
> This is negative framing and slightly manipulative. The prospect notices.

---

## Personalization Rules

- `{{personalization}}` must map to an evidence object with `observation`, `source`, and `verified: true`.
- Job title and company name are targeting context, not personalization evidence.
- Never infer intent from a hire, funding event, tool install, or content view; state only what the source supports.
- If a lead lacks verified evidence, leave the field empty and use segment-level relevance or remove the variable.

---

## Subject Lines

- Length: 3-7 words is the sweet spot
- No exclamation points
- No all-caps
- No emoji in B2B cold email (unless targeting a persona that expects it)
- Best patterns:
  - Question: "Quick question, {{firstName}}"
  - Observation: "{{companyName}}'s content strategy"
  - Specificity: "Saw your post on [topic]"
  - Intrigue: "One thing we noticed"
- Test one major variable at a time. Choose the winner using the preregistered primary outcome after the minimum sample, not open rate alone.

---

## Tone

- Peer-to-peer, not vendor-to-prospect
- Curious, not desperate
- Specific, not generic
- Short, not comprehensive
- Human, not corporate

If it sounds like a marketing email, rewrite it. Cold email that converts sounds like a text from a knowledgeable peer.

---

## Diagnosis order

When the primary outcome misses its threshold, inspect delivery and bounce guardrails first, then audience quality, evidence coverage, offer, sequence, and CTA. Change one major assumption in the next wave so the result remains interpretable.
