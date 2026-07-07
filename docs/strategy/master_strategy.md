# FABIABox Master Marketing Strategy

> **Thesis:** FABIABox’s first marketing objective is to prove market demand by driving product interest and shop purchases. Investor conversations are intentionally sequenced **after** measurable traction, because a Pre-Seed SAFE is easier to close with a live funnel than with a slide deck.

---

## 1. Strategic intent

1. **Primary goal (next 90 days):** generate qualified product interest and convert it into actions on [shop.fabiabox.com](https://shop.fabiabox.com).
2. **Secondary goal (after traction gates):** use that traction to raise a €500k–€1M Pre-Seed SAFE from European angels and micro-VCs.
3. **Long-term goal:** build a repeatable, agentic marketing pipeline that can scale both tracks in parallel.

---

## 2. Two-track model

| Track | Primary audience | Purpose | When active |
|-------|------------------|---------|-------------|
| **Traction** | Non-technical entrepreneurs, solopreneurs, small agencies, technical founders | Shop visits, trials, subscriptions, hardware reservations | Now – 90 days |
| **Investor** | European angels, pre-seed/seed VCs, syndicate leads | SAFE conversations, data-room access, pitch meetings | After traction gates are hit |

The two tracks share the same brand narrative, but the **message emphasis** changes:

- **Traction message:** “I have an idea and documents → FABIABox ships my product/company.”
- **Investor message:** “We have paying users, a waitlist, and pre-orders → this is the infrastructure layer for the agentic company era.”

---

## 3. Shared positioning

### Core tagline

> **The AI Co-Founder That Ships Your Company.**

### Supporting pillars

| Pillar | Traction framing | Investor framing |
|--------|------------------|------------------|
| **Ship** | From idea + documents to launched product | Productised company-creation at scale |
| **Sovereign** | You own the stack, the data, the model | Defensible infrastructure, not SaaS rent |
| **Speed** | Days/weeks, not months | Capital-efficient execution via agents |
| **Transparent pricing** | €49.99/mo or €499/yr plans; €500 hardware reservation | Healthy unit economics, recurring revenue + high-ticket hardware |
| **Human-in-the-loop** | Legal signatures pause for you | Governance model that scales trust |

---

## 4. Audience matrix

| Segment | Profile | Primary need | Likely first product | Overlap with investors |
|---------|---------|--------------|----------------------|------------------------|
| **Aspiring founder** | Non-technical, has idea/docs, limited budget | Validate and build an MVP | Agentic Build Plan | Low — they are users, not investors |
| **Solo operator** | Consultant/creator who wants to productise services | Automate delivery | Agentic Operate Plan | Low |
| **Technical founder** | Has AI/ML skills, wants sovereign hardware | Local, high-performance AI workstation | FABIABox Entry / Edge / Pro | Medium — may become angels |
| **Small agency** | Wants white-label AI agents for clients | Deploy and operate for multiple brands | Agentic Operate Plan / Premium tiers | Medium |
| **Enterprise innovator** | CTO/innovation lab, compliance-sensitive | On-premise AI infrastructure | FABIABox Enterprise | High — corporate venture arms |

**Priority order for traction:** Aspiring founder → Solo operator → Technical founder → Small agency → Enterprise innovator.

---

## 5. Channel priority map

### Traction phase

| Channel | Role | Priority |
|---------|------|----------|
| **Twitter/X** | Founder narrative, build-in-public, thread distribution | P0 |
| **LinkedIn** | B2B thought leadership, agency/enterprise reach | P0 |
| **Short-form video** (TikTok, YouTube Shorts, Reels) | Explainers for non-technical founders | P1 |
| **Email** | Nurture and convert waitlist/shop visitors | P0 |
| **SEO / research page / blog** | Long-term organic demand capture | P1 |
| **Discord / community** | Support, retention, product feedback | P1 |
| **Paid ads** | Amplify proven organic creative only | P2 (after organic baseline) |

### Investor phase

| Channel | Role | Priority |
|---------|------|----------|
| **Warm intros** | Highest-conversion SAFE conversations | P0 |
| **LinkedIn** | Direct outreach to angels/VCs, traction updates | P0 |
| **Investor newsletters / syndicates** | Deal-flow visibility | P1 |
| **Demo days / pitch events** | Batch meetings, social proof | P1 |
| **Data room + one-pager** | Due-diligibility | P0 |

---

## 6. Content pillars

All channels rotate around four pillars:

1. **Founder transformation** — “Before/after” stories of people who shipped a company with FABIABox.
2. **Process transparency** — How the AI co-founder pipeline works (idea → architect → market research → build → operate).
3. **Sovereign AI explainers** — Why owning your AI stack matters, without the vendor-lock-in jargon.
4. **Traction receipts** — Public milestones (waitlist size, MRR, units reserved) that also serve investor proof.

---

## 7. Automation stack

Reuse the architecture defined in [`../agents/best_practices.md`](../agents/best_practices.md):

| Layer | Tooling |
|-------|---------|
| Orchestration | LangGraph / CrewAI |
| Protocols | MCP for tools, A2A for agent communication |
| Content | LLM generation + brand-voice guardrails |
| Publishing | APIs for X, LinkedIn, TikTok, YouTube, email |
| Analytics | SQLite/Qdrant for campaign data + platform APIs |
| Human gate | Legal/billing/high-stakes posts require approval |

---

## 8. Metrics & traction gates

### Traction phase KPIs

| Metric | 30-day target | 90-day target |
|--------|---------------|---------------|
| Shop visits | 1,000 | 10,000 |
| Email waitlist | 250 | 1,000 |
| Agentic plan trials/purchases | 20 | 100 |
| Hardware reservations (€500) | 10 | 50 |
| Organic social impressions | 50,000 | 500,000 |
| Cost per qualified lead (paid) | Not active yet | < €25 |

### Investor activation gates

Activate the investor track only when **at least two** of the following are true:

- ≥ 50 paying Agentic plan customers **or** ≥ €2.5k MRR
- ≥ 50 hardware reservations (€500 each) = €25k committed
- ≥ 1,000 qualified waitlist subscribers with product-interest data
- A repeatable organic content-to-shop funnel with known conversion rate

---

## 9. 90-day roadmap

| Phase | Weeks | Focus | Key deliverables |
|-------|-------|-------|------------------|
| **Foundation** | 1–2 | Brand voice, shop funnel, analytics, email capture | Style guide, shop tracking, welcome sequence |
| **Organic engine** | 3–6 | Daily X/LinkedIn, 2 short videos/week, 1 blog/week | Content calendar, first case study, 250 waitlist |
| **Conversion** | 7–10 | Email nurture, retargeting, community, partnerships | Drip sequences, Discord, affiliate/ref pilot |
| **Optimisation** | 11–12 | Double down on winning channels, prepare investor pack | Metrics report, one-pager, data room skeleton |

---

## 10. Risks & assumptions

| Risk | Mitigation |
|------|------------|
| Non-technical founders don’t understand “sovereign AI” | Lead with outcomes, not infrastructure vocabulary |
| Hardware supply/timing uncertain | Sell reservations, not delivery commitments; be transparent |
| Agentic plans under-price support | Cap monthly active builds, offer upsells |
| Organic reach declines | Build email list as owned channel; paid only amplifies winners |
| Investor track delayed by traction | Keep investor materials lightweight and update monthly |

---

## 11. Next actions

1. Finalise the traction strategy details in [`traction_strategy.md`](traction_strategy.md).
2. Build the lightweight investor pack skeleton in [`investor_strategy.md`](investor_strategy.md) so it is ready when gates are hit.
3. Update the repo automation backlog to schedule the first 30 days of content.
