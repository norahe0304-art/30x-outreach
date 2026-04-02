# Cold Outreach Intelligence Brief — April 2026
**Research run date:** 2026-04-02
**Sources scanned:** 5 platforms, 3 community sources, 4 expert frameworks, GitHub topic index
**Confidence:** High on frameworks/schema; Medium on star counts (live GitHub data varies)

---

## 1. ICP Template — Best Fields Across Leading Frameworks

### Current Consensus: 4-Category Model

Every top framework (Apollo, Clay, Salesmotion, Sybill, Cognism, Becc Holland's Flip the Script) converges on the same 4 structural categories. The differentiation is in the fields within each category.

---

### Category 1: Firmographics (40 pts in 100-pt scoring models)

| Field | Source Consensus | Notes |
|-------|-----------------|-------|
| Industry / vertical | Universal | Primary + secondary + excluded |
| Employee headcount range | Universal | Min / max / sweet spot |
| Annual revenue or ARR | Universal | Range not exact |
| Funding stage | Apollo, Clay, Instantly | Bootstrapped / Series A+ / PE-backed |
| Business model | Salesmotion, Cognism | B2B SaaS / agency / marketplace / PLG |
| Geographic market | Universal | Country / region / language |
| Company growth rate | Clay, Apollo 2026 | Hiring velocity as proxy |
| HQ vs distributed | Niche signal | Useful for event-based targeting |

---

### Category 2: Technographics (30 pts)

| Field | Source Consensus | Notes |
|-------|-----------------|-------|
| CRM platform | Apollo, Clay, Clearbit | Salesforce / HubSpot / Pipedrive |
| Marketing automation | Clay, Clearbit | Marketo / HubSpot / Klaviyo |
| Data stack | Clay | Signal for data maturity |
| Competitive / adjacent tools | Clearbit, Apollo | Indicates switching potential |
| Tech stack complexity | Clay waterfall | Simple vs enterprise stack |

Clearbit adds 100+ data points; Clay pulls from 100+ providers via waterfall enrichment. Neither publishes a canonical field list publicly — they expose it through their UI.

---

### Category 3: Behavioral & Intent Signals (30 pts)

| Field | Source | Signal type |
|-------|--------|-------------|
| Pricing page visits | HubSpot, 6sense, Demandbase | Hot intent |
| Content downloads / webinar | Apollo, HubSpot | Warm intent |
| Job listings for target role | Clay (Claygent scraper) | Proxy for budget/initiative |
| LinkedIn engagement | Clay, Apollo | Awareness signal |
| Demo request history | CRM | Highest intent |
| G2 / Capterra reviews of competitors | Clay | Switching signal |
| Bombora intent data | Apollo (65+ filters) | Keyword-level research behavior |

Apollo's 65+ filters explicitly include Bombora-powered intent signals as of 2025.

---

### Category 4: Trigger Events (time-sensitive, highest conversion lift)

| Trigger | Source | Typical conversion lift |
|---------|--------|------------------------|
| Funding round (last 6 months) | Clay, Apollo, Crunchbase | 2-3x |
| New VP/CXO hire | Clay (LinkedIn job change) | 1.5-2x |
| Product launch in last 90 days | Claygent web scraper | 1.5x |
| Headcount growth > 20% YoY | Clay, Apollo | 1.5x |
| Running paid search (SpyFu/SEMrush) | Custom enrichment | Intent signal |
| Company moved to new office | Minor signal | Useful for localized plays |

---

### Anti-ICP Fields (Negative Scoring — Underused, High Value)

Apollo's 2026 ICP model explicitly builds in negative ICP signals. These should be documented:
- Historical churn indicators in your vertical
- Budget constraint proxies (sub-10 employees, no funding, NGO)
- Misaligned use cases (e.g., pure enterprise only, no mid-market)
- Contact-level: no verified email, missing firstName, on opt-out list

---

### ICP Scoring Rubric (100-Point Model — Salesmotion 2026)

**Recommended: 8-15 criteria across the 4 categories.**

| Tier | Score Range | Recommended action |
|------|-------------|-------------------|
| Tier A | 80-100 | Pursue immediately — personalized sequence |
| Tier B | 50-79 | Nurture — lighter touch sequence |
| Tier C | 0-49 | Deprioritize — remove or hold |

Enterprise multiplier weighting:
- Strategic fit: 3x
- Authority + budget: 2x
- Technical fit: 2x
- Timing signals: 2x
- Firmographic fit: 1x

Apollo benchmark: Companies with well-defined ICPs see 68% higher account engagement and 33% higher conversion rates.

---

### Gap vs. Current `icp-template.md`

The existing template covers titles, industries, company size, geography, buying signals, anti-ICP, offer-to-ICP fit, objections, and personalization data availability. It is strong.

**Missing fields to consider adding:**
- Technographics section (CRM / MarTech stack fields)
- Behavioral intent signals (pricing page visits, G2 activity)
- Funding stage specifics (Crunchbase signal)
- ICP score threshold field (at what score do we include this lead?)
- Negative ICP scoring criteria (not just binary exclusions but weighted)

---

## 2. Cold Email Copy Frameworks — What Is Working in 2025-2026

### Framework 1: Instantly's 25% Reply Rate Formula (Structural)

Full anatomy:
```
Personalization + Value Prop + Target Niche (subsegment/location)
+ Target's Goals + Target's Value Props
+ Relevant Case Study + Cliffhanger Value Prop + CTA
```

17 named strategies, top 5 in active use:
1. One-sentence email — brevity wins with attention-constrained buyers
2. Research angle — request prospect's input before pitching
3. Permission-based — ask to send more before sending it
4. Guarantee-based — deliverability / asset / action guarantee reduces perceived risk
5. Prework / Free Audit — deliver upfront value, ask nothing first

Source: [Instantly Help Center](https://help.instantly.ai/en/articles/6570131-cold-email-copywriting-framework-we-use-to-get-400-replies-monthly)

---

### Framework 2: Josh Braun's 4-Sentence Formula

Used by his "Badass B2B Growth" community. Anti-pitch philosophy.

```
Sentence 1 — Demonstrate research (evidence of homework on this specific prospect)
Sentence 2 — Highlight their challenge (fear of loss > promise of gain)
Sentence 3 — Solution + Social proof (similar companies you've helped)
Sentence 4 — Low-pressure CTA ("I'm not sure if this is a fit, but...")
```

The 4-T Framework (Braun variant):
- **T1 — Truth:** A factual observation about a specific problem you solve
- **T2 — Think:** A question that challenges how they're currently solving it
- **T3 — Third-party credibility:** Social proof or external validation
- **T4 — Talk:** A binary yes/no or a "free taste" CTA

Signature language patterns: use "no" and "without" — e.g., "No back-and-forth emails" or "Determine payouts without hard-pasting Excel sheets." Emotionally charged language over facts.

Test 3 variations over 4-6 weeks before declaring a winner.

Source: [Josh Braun](https://joshbraun.com/how-to-get-a-35-cold-email-response-rate/)

---

### Framework 3: Becc Holland's Flip the Script — 3-Line Structure

Strict 3-line format (max 4 lines):

```
Line 1 (longest) — Premise / reason for outreach. Must be specific.
Line 2 — Value proposition (1 sentence)
Line 3 — Call to action
```

The 4 Personalization Categories (Holland):
1. **Demographic** — person's role, title, education
2. **Technographic** — their technology stack signals right-fit
3. **Firmographic** — company size, industry, funding
4. **Psychographic** — values, passions, identity markers (highest response rate)

Holland's sequence structure: 21-day campaign, 4 touches Day 1-2, 3 touches every other day, breakup email at end.

The "Hook" framework (3 parts): premise + hook + relevance. Three ways to open a hook — specific observation, shared context, or contrarian insight.

Source: [Flip the Script](https://www.flipthescript.com/)

---

### Framework 4: Alex Berman's 3C Method + 30/30/50 Rule

3C Method (agency standard):
```
C1 — Compliment (specific, not generic)
C2 — Case Study (relevant proof)
C3 — Call to Action (direct ask)
```

30/30/50 Rule:
- 30% of success = targeting accuracy
- 30% of success = offer quality
- 50% of success = deliverability

The Baking Method: Year-long follow-up sequence for B2B. Drip over 12 months with periodic new angles rather than a 4-step burn.

Source: [Alex Berman](https://alexberman.com/)

---

### 2026 Benchmark Data (Instantly Cold Email Report)

| Metric | Average | Elite (Top 10%) |
|--------|---------|----------------|
| Reply rate | 3.43% | 10.7%+ |
| Top quartile | — | 5.5%+ |
| Optimal email length | — | Under 80 words |
| Optimal sequence length | — | 4-7 touchpoints |
| First-touch reply share | 58% | — |
| Follow-up reply share | 42% | — |

**Timing:** Launch Monday, peak follow-up engagement Wednesday, Friday for triage.

Source: [Instantly Benchmark Report 2026](https://instantly.ai/cold-email-benchmark-report-2026)

---

### What the Research Adds to Existing `copy-rules.md`

The current `copy-rules.md` is aligned with all frameworks. Specific additions worth incorporating:
- Add Becc Holland's 3-line strict format as a named variant
- Add Josh Braun's 4-T framework as a named variant for top-of-funnel
- Add the 30/30/50 rule as a campaign-level diagnostic, not just copy-level
- Explicitly document that 58% of replies come from Step 1 — this justifies spending the most iteration budget on Step 1

---

## 3. Company Intelligence Automation — Data Points and Approaches

### Clay's Enrichment Architecture

Clay functions as a data orchestration hub, not a single data source. Its primary mechanism:

**Waterfall Enrichment:** Stack multiple data providers in sequence. Each provider is queried only if the prior one did not return a result. Cost-optimized: cheap sources first, expensive sources last.

**Claygent (AI Scraper):** Web scraper with a natural language interface — can answer questions about a company by reading its website, LinkedIn, job boards, or any public URL. Single-click activation.

**100+ data providers connected**, including: Clearbit, Hunter, Dropcontact, People Data Labs, LinkedIn, Crunchbase, Apollo, ZoomInfo, and more.

**Data points Clay collects / enriches:**

| Category | Specific fields |
|----------|----------------|
| Company basics | Name, domain, description, HQ location, founded year |
| Firmographics | Industry, headcount, revenue range, growth rate |
| Funding | Round type (Seed/A/B/C), amount, date, investors |
| Leadership | CEO, CTO, CMO names + LinkedIn URLs |
| Tech stack | CRM, marketing automation, analytics, infrastructure tools |
| Hiring signals | Job postings count, roles being hired, department growth |
| Web presence | Traffic estimates, SEO metrics, ad spend proxies |
| Social | LinkedIn followers, Twitter/X followers, engagement rate |
| Contact-level | Full name, title, work email, personal email, LinkedIn URL, phone |
| Tenure | How long a contact has been in current role |
| Job change | Whether contact recently changed companies |

---

### Apollo's Intelligence Collection

Apollo combines enrichment + outreach in one platform. Key data points:

**65+ filters for lead search** including:
- Firmographics: industry, headcount, revenue, geography, business model
- Technographics: CRM, MarTech stack
- Seniority: C-level / VP / Director / Manager
- Keyword: job description keywords, company description keywords
- Intent: Bombora-powered keyword-level research behavior
- Engagement: email open history, click history (within Apollo sequences)

**Enrichment refresh:** CRM records refreshed continuously. As of 2025, CSV enrichment includes all available phone number types.

**Apollo's agentic direction (2025-2026):** "AI Projects" learn and improve over time. AI Assistant auto-generates personalized messaging from enriched data. Direction toward fully agentic GTM.

---

### Clearbit (Now HubSpot Breeze Intelligence)

Clearbit adds 100+ data points in seconds. Key differentiator: real-time CRM enrichment, refreshing Salesforce / HubSpot records every 30 days automatically.

Best for: companies that want passive enrichment of inbound leads rather than outbound prospecting lists.

---

## 4. Cold Email Quality Scoring — Expert Panel Framework

### What Exists (Already in This Repo)

The `expert-panel.md` file in this repo contains a well-designed 10-expert panel with named scoring lenses per panelist. This is the strongest open framework found for cold email quality scoring. No comparable open-source rubric was found that outperforms it.

**The panel covers:**
- Reply rate potential (Berman)
- Frame and status signaling (Klaff)
- Prospect respect / non-pushiness (Braun)
- Pattern interrupt / opening hook (Holland)
- Research depth and specificity (McKenna)
- Sequence architecture and value escalation (Coleman)
- Readability and reply signals (Allred)
- Deliverability and spam risk (Donovan)
- Pipeline math and multi-channel logic (Blount)
- LinkedIn integration potential (Dang)

---

### Scoring Rubric Dimensions — Consensus Across Sources

A scoring rubric for email quality should evaluate these 10 dimensions (synthesized from Instantly benchmarks, Salesmotion, Prospeo, and community sources):

| Dimension | What to evaluate | Weight |
|-----------|-----------------|--------|
| 1. Subject line | Length (2-4 words), personalization, no spam triggers | 10 pts |
| 2. Opening hook | Specific, not "I", earns next sentence | 15 pts |
| 3. Personalization | Real, company-specific, not token-substitution | 15 pts |
| 4. Value proposition | Clear, 1-2 sentences, tied to prospect's pain | 15 pts |
| 5. Social proof | Brief, credible, not fabricated | 10 pts |
| 6. CTA | Low-friction, single ask, no calendar link in Step 1 | 15 pts |
| 7. Length | Under 80 words for Step 1 | 5 pts |
| 8. Deliverability safety | No spam words, no links in Step 1, no attachments | 10 pts |
| 9. Tone | Peer-to-peer, not corporate or salesy | 5 pts |
| 10. Sequence logic | New angle per step, no "just checking in" | — (sequence-level) |

**Total: 100 points**
- 90+: Ready to send
- 75-89: Revise 1-2 dimensions
- Under 75: Rewrite

---

### External Tools for Email Quality Scoring

| Tool | URL | What it scores |
|------|-----|---------------|
| FirstSales Email Scorer | firstsales.io/tools/email-quality-scorer | Free, web-based quality check |
| Lavender (Will Allred) | lavender.ai | AI reply-rate scoring, readability grade, mobile preview |
| Mailreach | mailreach.co | Deliverability-specific scoring, spam word detection |
| Sender Score | senderscore.org | Domain/IP reputation scoring |

---

## 5. Open-Source Cold Outreach Repos on GitHub

Honest assessment: the open-source cold outreach ecosystem on GitHub is thin. Most serious practitioners use SaaS tools (Instantly, Smartlead, Lemlist). The best-architected open tooling lives in AI agent wrappers.

| Repo | Stars | Language | Architecture notes | URL |
|------|-------|----------|-------------------|-----|
| meteor-emails | 147 | JavaScript | SendGrid SMTP, free, basic campaign management | github.com/catin-black/meteor-emails |
| Email-automation (PaulleDemon) | 130 | Python/Django | Django + Celery + PostgreSQL + Redis, Jinja2 templates, follow-up rules, Railway/Render deployable — best architecture in the list | github.com/PaulleDemon/Email-automation |
| GPT_email_generator | 82 | Python | GPT-3 email generation from user input, no campaign mgmt | github.com/stefanrmmr/GPT_email_generator |
| map-email-scraper | 85 | JavaScript | Scrapes contact details from public business listings | github.com/MickeyUK/map-email-scraper |
| AI-agent-for-cold-emails (Ionio) | 15 | Jupyter/Python | LangChain + Apollo + Smartlead integrations, RAG on past emails for tone matching, agentic inbox management | github.com/Ionio-io/AI-agent-for-cold-emails |
| coldflow | 7 | TypeScript | "Open Source Cold Email That Actually Works", early stage | github.com/pypes-dev/coldflow |
| ai-marketing-skills (ericosiu) | — | Python | This repo — most complete open framework for agent-driven outbound found in the search | github.com/ericosiu/ai-marketing-skills |

**Assessment:** PaulleDemon/Email-automation has the best standalone architecture (130 stars). The Ionio AI-agent repo has the most interesting agentic design pattern (Apollo + Smartlead + RAG) at only 15 stars — worth watching. No open-source repo currently competes with the full pipeline architecture in `scripts/lead-pipeline.py`.

---

## 6. Standard Lead Data Schema — Essential vs Nice-to-Have

### Apollo CSV Export Fields (confirmed via Apollo docs + community)

**Contact-level essential:**

| Field | Required for outreach | Notes |
|-------|--------------------|-------|
| First Name | Yes — required for personalization | Missing = do not send |
| Last Name | Yes | |
| Work Email | Yes — verified status matters | Unverified = higher bounce risk |
| Job Title | Yes — for ICP qualification | |
| LinkedIn URL | Yes — for research + multichannel | |
| Company Name | Yes — required for personalization | |
| Company Website | Yes — for enrichment + deduplication | |
| Apollo Contact ID | Yes — for deduplication | |

**Contact-level nice-to-have:**

| Field | Use case |
|-------|---------|
| Phone (mobile/direct) | Multichannel sequences (LinkedIn + call) |
| City / State / Country | Geo-personalization, local language plays |
| Seniority level | Routing logic (VP vs Director vs Manager) |
| Department | Segmentation |
| Years at company | Job change signal |

**Company-level essential:**

| Field | Required | Notes |
|-------|----------|-------|
| Company Name | Yes | |
| Domain | Yes — for deduplication + enrichment | |
| Industry | Yes — ICP filtering | |
| Employee Count | Yes — ICP filtering | |
| HQ Country | Yes — geo targeting | |

**Company-level nice-to-have:**

| Field | Use case |
|-------|---------|
| Annual Revenue / ARR | Budget signal |
| Funding Stage + Last Round Date | Trigger event targeting |
| Tech Stack (CRM, MAP) | Technographic ICP matching |
| LinkedIn Company URL | Enrichment source |
| Headcount Growth % | Buying signal |
| Hiring for [role] | Intent signal |
| G2 / review site presence | Competitor research signal |

---

### Instantly Import Schema (confirmed from community + docs)

Instantly accepts CSV import with these mapped fields:

| Field name | Type | Required |
|-----------|------|---------|
| email | string | Yes |
| first_name | string | Strongly recommended |
| last_name | string | Recommended |
| company_name | string | Recommended |
| website | string | Optional |
| Any custom variable | string | Optional — maps to `{{variable_name}}` in templates |

Instantly's key constraint: custom variables are unlimited but must be pre-defined as column headers in the CSV. The `{{personalization}}` variable pattern used in `icp-template.md` maps directly to this schema.

---

### Clay's Lead Schema (Internal Model)

Clay stores data in a spreadsheet-like table where columns = data fields. Standard columns built during a Clay enrichment workflow:

**From Apollo enrichment:**
first_name, last_name, email, title, linkedin_url, company_name, company_domain, company_industry, company_headcount, company_location, company_revenue_range

**From Clay-native enrichment (Claygent + waterfall):**
funding_round, funding_amount, funding_date, tech_stack, hiring_signals, company_description, recent_news, decision_maker_linkedin, tenure_in_role, recent_job_change

**From custom Claygent research:**
Any natural language field — e.g., "What is their main product?", "Do they have a dedicated SDR team?", "What CRM are they using?"

---

## Strategic Recommendations for This Repo

**ICP Template (`icp-template.md`)**
1. Add a Technographics section with CRM / MarTech fields
2. Add intent signal fields (pricing page visits, job posting signals, Bombora)
3. Add a numeric ICP score threshold field — at what score does a lead qualify?
4. Add negative ICP scoring criteria as weighted fields, not just binary exclusions

**Expert Panel (`expert-panel.md`)**
The panel is comprehensive and aligns with current expert consensus. No changes needed. Consider adding a Tier B panel for specific industries: Lou Adler (HR tech), Jason Lemkin (SaaS), John Barrows (enterprise).

**Copy Rules (`copy-rules.md`)**
1. Add Becc Holland's 3-line format as a named variant
2. Add Josh Braun's 4-T framework as a named variant
3. Document the 58% / 42% split (Step 1 vs follow-ups) to justify iteration budget
4. Add the 30/30/50 rule (targeting / offer / deliverability) as a campaign diagnostic

**Lead Schema (`scripts/lead-pipeline.py`)**
The Apollo → LeadMagic → Instantly pipeline covers the essential schema. Consider adding:
- `funding_date` as a trigger event field (requires Crunchbase or Clay enrichment)
- `tech_stack_crm` as a technographic field (requires Clay waterfall or BuiltWith)
- `days_in_role` to flag recently-hired decision makers (requires LinkedIn enrichment)

---

## Sources

- [Instantly Cold Email Framework](https://help.instantly.ai/en/articles/6570131-cold-email-copywriting-framework-we-use-to-get-400-replies-monthly)
- [Instantly 2026 Benchmark Report](https://instantly.ai/cold-email-benchmark-report-2026)
- [Josh Braun — 35% Reply Rate Framework](https://joshbraun.com/how-to-get-a-35-cold-email-response-rate/)
- [Josh Braun — Cold Email Learn](https://joshbraun.com/learn/cold-email/)
- [Josh Braun LinkedIn — 4-T Framework](https://www.linkedin.com/posts/josh-braun_heres-a-cold-email-copywriting-framework-activity-6963097038074880000-uqFf)
- [Alex Berman — Official Site](https://alexberman.com/)
- [Becc Holland — Flip the Script](https://www.flipthescript.com/)
- [Becc Holland — Personalization Webinar](https://www.flipthescript.com/personalization-to-relevance-webinar)
- [Apollo — ICP in Sales (2026)](https://www.apollo.io/insights/icp-meaning-sales)
- [Salesmotion — ICP Scoring Rubric 2026](https://salesmotion.io/blog/ideal-customer-profile-template)
- [Clay — ICP Glossary](https://www.clay.com/glossary/ideal-customer-profile)
- [Clay University — Find ICP with AI](https://www.clay.com/university/lesson/find-your-icp-with-ai)
- [OutreachArk — AI-Powered GTM Apollo + Clay 2025](https://www.outreachark.com/blog/ai-powered-gtm-apolloio-clay-agentic-end-to-end-platforms-2025)
- [Pintel — Lead Enrichment Tools Compared](https://pintel.ai/blogs/lead-enrichment-tools-compared-apollo-clay/)
- [Sybill — ICP Guide 2026](https://www.sybill.ai/blogs/icp-guide)
- [GitHub — cold-emails topic](https://github.com/topics/cold-emails)
- [PaulleDemon/Email-automation](https://github.com/PaulleDemon/Email-automation)
- [Ionio-io/AI-agent-for-cold-emails](https://github.com/Ionio-io/AI-agent-for-cold-emails)
- [Apollo CSV Export Docs](https://knowledge.apollo.io/hc/en-us/articles/4409237712141-Export-Contacts-to-a-CSV)
- [Apollo Import CSV Docs](https://knowledge.apollo.io/hc/en-us/articles/4409161532045-Import-a-CSV-of-Contacts)
- [Prospeo — Lead Scoring for Cold Email 2026](https://prospeo.io/s/lead-scoring-for-cold-email)
- [FirstSales Email Quality Scorer](https://firstsales.io/tools/email-quality-scorer/)
