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
| AdSet | `EU Founders` (consolidated single adset) |
| Active ads | 6 creative variants (V1–V6) |
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

Single consolidated adset to speed up learning and avoid clutter:

```
Campaign: FABIABox — Website Retargeting
 ├── AdSet: EU Founders
 │   ├── Ad V1: Founder with idea
 │   ├── Ad V2: Product shot
 │   ├── Ad V3: Own the stack / ship fast
 │   ├── Ad V4: Timeline / speed
 │   ├── Ad V5: Product close-up
 │   └── Ad V6: Co-founder metaphor
```

Core messaging:

> **The AI Co-Founder That Ships Your Company.**

Target: non-technical European entrepreneurs, pre-seed/seed stage, English-speaking EU.

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

- Pause any creative with **< 0.5% CTR** after ~3,000 impressions.
- Scale budget on any creative with **> 2% CTR** and cost-per-click under target.
- Keep only one adset while learning budget is small; split audiences only after 50+ conversions per week.
- Refresh ad copy/images every 4–6 weeks to avoid fatigue.

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

*Last updated: 2026-07-07*  
*Author: Andrea (IABAI)*
