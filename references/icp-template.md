# ICP Data Collection Template

> [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

Use this template when defining the Ideal Customer Profile. Collect all fields before writing copy.
After collection, persist to `data/icps/{name}/profile.json`.

---

## ICP Definition

**ICP Name:** _______________ (slug format: `saas-vp-marketing`, `ecom-founders`)
**Client/Campaign:** _______________
**Date:** _______________

---

### Target Titles
Who specifically receives these emails?

**Primary titles (high intent):**
- e.g., VP of Marketing
- e.g., Director of Demand Generation
- e.g., Head of Growth

**Secondary titles (acceptable, lower priority):**
- e.g., CMO (at smaller companies)
- e.g., Marketing Manager (if company size <50)

**Never target:**
- e.g., Coordinators, Interns, Assistants (unless specifically requested)

---

### Target Industries / Verticals

**Primary verticals:**
1.
2.
3.

**Secondary verticals (test, not primary):**
1.
2.

**Excluded verticals (anti-ICP):**
- e.g., Non-profits (budget constraints)
- e.g., Government (procurement timelines)

---

### Company Size

**Employee count range:**
- Minimum: ___
- Maximum: ___
- Sweet spot: ___

**Revenue range (if targeting by revenue):**
- Minimum ARR/Revenue: $___
- Maximum: $___

**Funding stage (if relevant):**
- e.g., Series A+
- e.g., Bootstrapped >$5M revenue
- e.g., PE-backed

---

### Geographic Targeting

**Primary markets:**
- e.g., US only
- e.g., US + Canada
- e.g., English-speaking markets

**Excluded regions:**
- e.g., APAC (different sales motion)

---

### Buying Signals / Trigger Events

What makes a company more likely to buy right now?

- e.g., Recently hired a new VP Marketing (job posting signal)
- e.g., Raised funding in last 6 months
- e.g., Launched new product in last 90 days
- e.g., Running paid search (visible via SpyFu/SemRush)
- e.g., Job listings for [role] signal they need help
- e.g., Tech stack includes [specific tool] (via BuiltWith/Wappalyzer)
- e.g., Website traffic growing >20% MoM (via SimilarWeb)

---

### Anti-ICP (Explicit Exclusions)

Who should never receive these emails?

**Company characteristics:**
- e.g., <10 employees (too small, no budget)
- e.g., Bootstrapped and not scaling
- e.g., Already a current client
- e.g., Competitors

**Contact characteristics:**
- e.g., No verified email (bounce risk)
- e.g., Missing firstName (won't personalize)
- e.g., Opt-out list

---

### Offer-to-ICP Fit

**What's the primary offer?**
- [ ] Free audit
- [ ] Free trial
- [ ] Demo
- [ ] Strategy call
- [ ] Content/report download
- [ ] Other: _______________

**Why this offer for this ICP?**
(One sentence — if you can't answer this, the offer needs rethinking)

---

### Known Objections

What does this ICP typically say no to?

1.
2.
3.

**How to neutralize in copy:**
(Pick the one that kills the most deals. Neutralize it in Step 3 or 4 — not Step 1)

---

### Technographics (Tech Stack Signals)

What tools does the ideal target company use?

**CRM / Marketing automation:**
- e.g., HubSpot, Salesforce, Marketo
- e.g., No CRM = early stage, may need more education

**Adjacent / Competitor tools:**
- e.g., Uses [competitor product] = aware of category, easier sell
- e.g., Uses [complementary tool] = integration opportunity

**Data stack maturity:**
- [ ] Basic (spreadsheets, no CRM)
- [ ] Growing (CRM + basic automation)
- [ ] Mature (full stack: CRM + automation + analytics + enrichment)

**Sources:** BuiltWith, Wappalyzer, Apollo technographic filters, Clay enrichment

---

### Behavioral Intent Signals

What online behaviors indicate readiness to buy?

- e.g., Researching your category keywords (Bombora intent data via Apollo)
- e.g., Visiting competitor G2/Capterra pages
- e.g., Downloading industry reports / attending webinars
- e.g., LinkedIn engagement with relevant content
- e.g., Website traffic growth >20% MoM (SimilarWeb)

**Intent data sources:**
- [ ] Bombora (via Apollo)
- [ ] G2 buyer intent
- [ ] LinkedIn engagement
- [ ] Website visitor identification (RB2B / Clearbit)
- [ ] None available

---

### Personalization Data Available

What data fields are available per lead?

- [ ] firstName (required)
- [ ] companyName (required)
- [ ] personalization field — source: _______________
- [ ] Industry
- [ ] Employee count
- [ ] LinkedIn URL
- [ ] Recent funding round
- [ ] Recent job posting
- [ ] Tech stack signals
- [ ] Other: _______________

**Personalization source:**
- e.g., Clay enrichment
- e.g., Apollo export
- e.g., Manual research (for small lists)
- e.g., None (template must work without it)

**Personalization strategy:**
- High-touch (<100 leads): manual research per lead
- Medium-touch (100-500): Clay/Apollo enrichment + template
- Scale (500+): template-only, {{personalization}} field optional

---

### Apollo Search Parameters

Map ICP to Apollo API fields (auto-populated by Claude when saving profile.json):

```json
{
  "person_titles": ["VP Marketing", "Head of Growth"],
  "q_organization_keyword_tags": ["SaaS", "B2B"],
  "organization_num_employees_ranges": ["11,50"],
  "person_locations": ["United States"],
  "q_keywords": ""
}
```

---

### Notes / Special Instructions

Any other context the copywriter needs:

_______________
