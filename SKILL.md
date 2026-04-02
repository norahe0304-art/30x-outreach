---
name: 30x-outreach
description: End-to-end cold outbound engine. Auto-profiles businesses (website scrape + founder interview), persists multi-ICP targeting, sources and verifies leads (Apollo→LeadMagic→Instantly), writes email sequences scored by 10-expert panel (recursive to 90+), monitors competitors, detects cross-signals, and sends with human approval gate. Use when building cold email campaigns, optimizing outbound, or managing ICPs.
argument-hint: <icp-name>
---

# 30x Outreach Engine

---

## Dynamic Context (auto-injected on skill load)

### Business Profile
!`cat ${CLAUDE_SKILL_DIR}/data/business/profile.json 2>/dev/null || echo '{"status": "NOT_CONFIGURED", "action": "Run Step 1 to set up business profile"}'`

### Active ICP
!`cat ${CLAUDE_SKILL_DIR}/data/icps/$0/profile.json 2>/dev/null || echo '{"status": "NOT_FOUND", "icp": "$0", "action": "Run Step 2 to create this ICP"}'`

### Latest Competitive Intel
!`cat ${CLAUDE_SKILL_DIR}/data/intel/competitive/latest.json 2>/dev/null || echo '{"status": "NO_DATA", "action": "Run Step 5 competitive-monitor.py"}'`

### Latest Cross-Signals
!`cat ${CLAUDE_SKILL_DIR}/data/intel/signals/latest.json 2>/dev/null || echo '{"status": "NO_DATA", "action": "Run Step 5 cross-signal-detector.py"}'`

---

## Startup Router

Check what's already configured and skip to the right step:

1. **No business profile?** → Step 1 (first-time setup, one-time only)
2. **Business profile exists, no ICP for `$0`?** → Step 2
3. **ICP exists?** → Step 3 (or whichever step user needs)

If user passes no argument (`/30x-outreach` with no ICP name):
- List existing ICPs from `data/icps/` directory
- Ask: "Which ICP do you want to work with, or create a new one?"

---

## Step 1: Business Intelligence (one-time setup)

**Goal:** Build a complete business profile from two parallel sources.

Ask: **"What's your domain?"**

Once you have the domain, run both paths simultaneously:

### Path A: Auto-Scrape
Use web tools to gather:
- **Homepage** → positioning, product description, value prop
- **Pricing page** → pricing model, tiers, price points
- **About page** → team size, founding story, mission
- **Case studies / testimonials** → social proof, client names, results
- **LinkedIn company page** → industry, employee count, description
- **Twitter/X** → tone of voice, recent topics, engagement style

### Path B: Founder Interview
Ask these questions (adapt based on what auto-scrape already found):

1. **What do you sell?** (one sentence, no jargon)
2. **Who's your ideal buyer?** (title + company type)
3. **What's your primary offer?** (free audit, demo, trial, consultation)
4. **Why do customers choose you over alternatives?** (real differentiator)
5. **What's your best proof point?** (specific result, named client if possible)
6. **Who are your top 3 competitors?**
7. **What's the #1 objection you hear?**
8. **What's your price range?** (helps calibrate ICP company size)

### Merge + Confirm
- Combine both sources into a unified profile
- **Flag conflicts** (e.g., website says "enterprise", founder says "SMB")
- Present to user for review and correction
- Save to `data/business/profile.json` and `data/business/brief.md`

---

## Step 2: ICP Definition

**Goal:** Create a targeting profile for a specific buyer persona.

Use `references/icp-template.md` as the collection framework, but tailor questions based on business profile context.

Collect:
- **Target titles** (primary + secondary + never-target)
- **Industries / verticals** (primary + secondary + excluded)
- **Company size** (employee range + revenue floor + funding stage)
- **Geography** (primary markets + excluded regions)
- **Buying signals** (job postings, funding, product launches, tech stack)
- **Anti-ICP** (explicit exclusions — company traits + contact traits)
- **Offer-to-ICP fit** (why this offer for this audience)
- **Known objections** (top 3 + how to neutralize in copy)
- **Personalization data sources** (Clay, Apollo, manual, none)

Save to:
- `data/icps/{icp-name}/profile.json` — structured data
- `data/icps/{icp-name}/brief.md` — human-readable summary

---

## Step 3: Infrastructure Audit

Run: `python3 scripts/instantly-audit.py`

Reports:
- Sending accounts: count, warmup score, daily limit
- Domain health: SPF/DKIM/DMARC status
- Capacity math: ready accounts × 30/day = conservative volume
- **Blockers:** accounts with warmup < 80 or < 14 days → flagged red

Output: `data/output/{date}-instantly-audit.json`

**Decision gate:** If zero accounts are ready → STOP. Do not proceed to lead sourcing.

---

## Step 4: Lead Pipeline

Run: `python3 scripts/lead-pipeline.py --icp {icp-name}`

The script reads `data/icps/{icp-name}/profile.json` for targeting parameters.

Pipeline:
1. **Apollo search** → source leads matching ICP criteria
2. **LeadMagic verify** → validate email addresses
3. **Instantly dedup** → remove already-contacted leads
4. **Batch upload** → 25 leads per batch to Instantly campaign

Output:
- `data/leads/{icp-name}/raw.json` — Apollo results
- `data/leads/{icp-name}/verified.json` — post-verification
- `data/leads/{icp-name}/uploaded.json` — final uploaded set

---

## Step 5: Competitive Intelligence + Cross-Signals

### Competitive Monitor
Run: `python3 scripts/competitive-monitor.py`

Reads competitor list from `config.json`. For each competitor:
- Fetch pricing page → snapshot + diff against previous
- Fetch blog → extract recent posts
- Auto-search LinkedIn + job boards (via Brave API / web search)
- Classify signals: 🔴 Threat / 🟡 Interesting / 🟢 Opportunity

Output: `data/intel/competitive/latest.json`

### Cross-Signal Detector
Run: `python3 scripts/cross-signal-detector.py`

Scans all module outputs in `data/output/` for overlapping:
- Company names appearing across multiple sources
- Industry verticals trending in multiple channels
- Keyword clusters showing cross-channel momentum

Output: `data/intel/signals/latest.json`

---

## Step 6: Email Sequence Creation + Expert Panel

### Input Context
The email writer has access to:
- `data/business/profile.json` — who you are, what you sell, proof points
- `data/icps/{icp-name}/profile.json` — who you're targeting, their pain points
- `data/intel/competitive/latest.json` — competitive landscape
- `references/copy-rules.md` — writing rules (hard constraints)
- `references/instantly-rules.md` — platform rules (variables, limits)

### Sequence Structure
Write a 5-6 step email sequence per `references/instantly-rules.md`:
- Step 1 (Day 0): Pattern interrupt + value + soft CTA. Max 3 sentences.
- Step 2 (Day 2): New angle or asset. 3-5 sentences.
- Step 3 (Day 4-7): Social proof or case study. 3-5 sentences.
- Step 4 (Day 7): Direct value or insight. 3-5 sentences.
- Step 5 (Day 7-14): Short bump. 1-2 sentences.
- Step 6 (Day 7-14): Breakup with genuine value. 2-3 sentences.

### Expert Panel Scoring
Use `references/expert-panel.md` for the 10-expert roster.

**Target: 90/100. Non-negotiable. Iterate until reached.**

Each round:
1. All 10 panelists score (0-100) with one-line rationale
2. Calculate aggregate average
3. If < 90: identify top 3 weaknesses, revise, run next round
4. If ≥ 90: finalize
5. Show every round — the iteration trail is part of the deliverable

### Copy Rules (hard constraints from `references/copy-rules.md`)
- Never start with "I" / "We" / "Our team"
- Soft CTAs only in Steps 1-3
- No links in Step 1
- Stats as observations, never as studies
- Never fabricate client names, numbers, or URLs
- Subject lines: 3-7 words, no caps, no emoji, no exclamation

---

## Step 7: Human Review Gate

Generate the complete deliverable document:

1. **Business + ICP Summary** — who you are, who you're targeting
2. **Infrastructure Status** — accounts ready, capacity math
3. **Lead Pipeline Summary** — sourced → verified → uploaded counts
4. **Competitive Intel Summary** — key threats and opportunities
5. **Email Sequence** — all steps, Instantly-ready format with valid variables only
6. **Expert Panel Record** — every scoring round with scores + changes
7. **Capacity Math** — accounts × daily send = monthly volume → expected replies → pipeline
8. **Weekly Metric Targets:**

| Metric | Good | Great |
|--------|------|-------|
| Open rate | 40%+ | 60%+ |
| Reply rate | 3%+ | 7%+ |
| Positive reply rate | 1%+ | 3%+ |
| Meeting rate | 0.5%+ | 1.5%+ |

**⛔ Do NOT send anything automatically. Wait for explicit "approved" from user.**

---

## Step 8: Send

Only after user says "approved":

Run: `python3 scripts/cold-outbound-sender.py`

- Reads approved prospects
- PII security scan (blocks API keys, passwords, local paths in email body)
- Daily send limit enforcement
- History tracking (no duplicate sends)

Output: `data/output/{date}-send-log.json`

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/copy-rules.md` | Email copy hard constraints |
| `references/expert-panel.md` | 10-expert scoring roster + lenses |
| `references/instantly-rules.md` | Instantly platform rules (variables, warmup, deliverability) |
| `references/icp-template.md` | ICP data collection framework |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/instantly-audit.py` | Pull Instantly campaigns, accounts, warmup scores |
| `scripts/lead-pipeline.py` | Apollo → LeadMagic → Instantly pipeline |
| `scripts/competitive-monitor.py` | Competitor pricing, blog, hiring signal tracking |
| `scripts/cross-signal-detector.py` | Cross-source signal overlap detection |
| `scripts/cold-outbound-sender.py` | Send approved emails with safety checks |

## Configuration

All API keys and settings in `config.json` at skill root. See `config.example.json` for template.
