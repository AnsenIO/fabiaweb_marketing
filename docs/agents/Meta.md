# Meta (Facebook & Instagram) Ads — FABIABox Marketing Runbook

> **Purpose:** Operate Meta Ads and the FABIABox Facebook page programmatically for FABIABox.

---

## Current setup

| Item | Value / Note |
|------|--------------|
| Page | SquadShelf → rebranding to **FABIABox** |
| Ad account | IABAI ad account, currency **EUR** |
| Active campaign | `FABIABox — Website Retargeting` |
| Objective | `OUTCOME_TRAFFIC` |
| AdSets | `US Founders` (€25), `EU Founders` (€20), `EU Founders (intent-qualified)` (€25), `EU VC & Accelerators` (€25), `US VC & Accelerators` (€25) |
| Active ads | V1–V6 + V3.1 in US/EU adsets; V3.1 + V4 + V5 in EU intent adset; V3.1 + V4 + V5 in EU/US VC adsets |
| Winning image hash | `6fdc8f0b5df6eea893dbcfac00a79b07` (used by V5 and V3.1) |
| Status | controlled by `META_AD_STATUS` env var (`PAUSED` or `ACTIVE`) |

---

## Authentication & token management

Meta uses three token types:

| Token | Lifetime | How we handle it |
|-------|----------|------------------|
| Short-lived User Access Token | ~1–2 hours | Generated in [Graph API Explorer](https://developers.facebook.com/tools/explorer/) |
| Long-lived User Access Token | ~60 days | Exchanged automatically via script; refreshable before expiry |
| Page Access Token | Never expires (if from long-lived user token) | Fetched automatically via `/me/accounts` |

### Required permissions

- `ads_management`
- `ads_read`
- `business_management`
- `pages_manage_metadata`
- `pages_read_engagement`

### Scripts

```bash
# Exchange a short-lived token and fetch the page token
cd ~/projects/fabiaweb_marketing
python scripts/get_meta_long_lived_token.py "<SHORT_LIVED_TOKEN>"

# Refresh an existing long-lived token before it expires
python scripts/get_meta_long_lived_token.py --refresh
```

The script updates `config/.env` with `META_ACCESS_TOKEN` and `META_PAGE_ACCESS_TOKEN` and writes the expiry to `config/meta_token_expiry.txt`.

---

## Campaign structure

Two geo-split adsets plus one intent-qualified EU adset to learn market-specific and audience-qualified response:

```
Campaign: FABIABox — Website Retargeting
 │
 ├─── AdSet: US Founders (€25/day)
 │   ├─── Ad V1: Human co-founder
 │   ├─── Ad V2: Functional co-founder
 │   ├─── Ad V3: Own the stack / ship fast (paused)
 │   ├─── Ad V3.1: AI co-founder + sovereign stack
 │   ├─── Ad V4: Hologram
 │   ├─── Ad V5: SaaS is dead / sovereign AI
 │   └─── Ad V6: Why rent AI / foundry
 │
 ├─── AdSet: EU Founders (€20/day) — broad geo
 │   ├─── Ad V1: Human co-founder (paused)
 │   ├─── Ad V2: Functional co-founder
 │   ├─── Ad V3: Own the stack / ship fast (paused)
 │   ├─── Ad V3.1: AI co-founder + sovereign stack
 │   ├─── Ad V4: Hologram
 │   ├─── Ad V5: SaaS is dead / sovereign AI
 │   └─── Ad V6: Why rent AI / foundry
 │
 └─── AdSet: EU Founders (€25/day) — intent-qualified (same interests as US)
     ├─── Ad V3.1: AI co-founder + sovereign stack
     ├─── Ad V4: Hologram
     └─── Ad V5: SaaS is dead / sovereign AI

 ├─── AdSet: EU VC & Accelerators (€25/day) — venture capital / seed accelerator / angel investor
 │   ├─── Ad V3.1: AI co-founder + sovereign stack
 │   ├─── Ad V4: Hologram
 │   └─── Ad V5: SaaS is dead / sovereign AI
 │
 └─── AdSet: US VC & Accelerators (€25/day) — venture capital / seed accelerator / angel investor
     ├─── Ad V3.1: AI co-founder + sovereign stack
     ├─── Ad V4: Hologram
     └─── Ad V5: SaaS is dead / sovereign AI
```

Core messaging:

> **YOUR AI CO-FOUNDER. SHIP YOUR COMPANY.**

Target: non-technical entrepreneurs, pre-seed/seed stage, US + English-speaking EU. The EU intent adset adds the US interest stack (small business, AI, startups, SaaS, entrepreneurship) to qualify cold traffic. The VC & Accelerators adsets test whether investors and accelerator networks respond to the sovereignty / local-AI message.

---

## Operational scripts

| Script | Purpose |
|--------|---------|
| `scripts/get_meta_long_lived_token.py` | Exchange/refresh tokens |
| `scripts/update_facebook_page.py` | Sync page name/about/website/phone (requires `pages_manage_metadata`) |
| `scripts/check_meta_health.py` | Daily account + campaign + ad + page status check |

### Daily health check

A cron job runs every morning at 09:00 CET and Telegrams the summary:

```bash
cron: meta-daily-health
command: cd /home/ansen/projects/fabiaweb_marketing && python scripts/check_meta_health.py
```

To run it manually:

```bash
python scripts/check_meta_health.py
```

It reports:
- Ad account status, spend cap, lifetime spend
- Campaign status and lifetime impressions/clicks/spend
- Ad status and lifetime performance per variant
- Facebook page name, about, website, phone, fan count

---

## Facebook page branding

Use this copy if updating the page manually:

| Field | Copy |
|-------|------|
| **Name** | FABIABox |
| **Username** | @fabiabox |
| **Category** | Software Company |
| **About** | The AI Co-Founder That Ships Your Company. |
| **Description** | Fabia is the AI Agent that turns your idea into a live product and business. Built for non-technical founders in Europe. Own your AI, your data, and your stack. |
| **Website** | https://fabiabox.com |
| **Phone** | +33 4 84 25 00 00 |
| **Company overview** | FABIABox helps founders go from idea to operating company using localized AI agents that build, launch, and run the business with you. |
| **Mission** | Make every founder capable of shipping a real company without renting their intelligence from a cloud provider. |
| **CTA button** | Learn More → https://fabiabox.com |

Page renames via the API can be rejected if the app lacks the right capability; if so, change the name directly in the Facebook UI and wait for review.

---

## Monitoring cadence

| Frequency | Action |
|-----------|--------|
| **Daily 09:00 CET** | Auto health check (account, campaigns, ads, page) |
| **Daily** | Sync leads from landing page / Meta forms |
| **Weekly** | Review CTR/CPC per creative; pause underperformers, scale winners |
| **~Day 55** | Refresh long-lived token with `--refresh` |
| **Monthly** | Budget pacing, audience refresh, new creative batch |

---

## Optimization rules

- Pause any creative with **< 1% CTR** after ~3,000 impressions.
- Scale budget on any creative with **> 3% CTR** and cost-per-click under €0.15.
- Keep one broad geo adset per market while learning budget is small.
- **Clone the winning audience into new regions:** the US adset outperformed the broad EU adset because it stacked interests on top of geo. The EU intent adset (`120249476780370462`) replicates the US targeting and runs only the top EU creatives + V3.1.
- Refresh ad copy/images every 4–6 weeks to avoid fatigue.
- **Learning to date:** V5 ("SaaS is dead") and V6 ("Why rent AI") are the volume winners; V2 ("Your AI co-founder") has the highest CTR but tiny reach. V3 worked in the US (7.94% CTR) but failed in the EU (1.64% CTR), so it was evolved into **V3.1** — same winning V5 image, a "co-founder" headline, and a primary text that pairs concrete deliverables (MVP, brand, go-to-market) with sovereignty (on your desk, your data, your control).

---

## Next steps

1. [x] Exchange long-lived token and fetch page token
2. [x] Create retargeting campaign with 6 creative variants
3. [x] Consolidate adsets into single `EU Founders` adset
4. [x] Schedule daily health-check cron
5. [ ] Complete Facebook page rename from SquadShelf to FABIABox
6. [ ] Set up Facebook Pixel events on fabiabox.com
7. [ ] Connect lead-capture form to Meta leads / CRM
8. [ ] Build lookalike audience once custom audience reaches 100+ people
9. [ ] Add LinkedIn and email channels to the loop

---

*Last updated: 2026-07-10*  
*Author: Andrea (IABAI)*
