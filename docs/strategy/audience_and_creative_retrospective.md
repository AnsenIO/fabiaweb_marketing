# Audience & Creative Retrospective — FABIABox

> Scope: the work done in the 24–48 h window before 2026-07-10, plus the state check on 2026-07-10.  
> Goal: understand who is actually visiting, which creatives are winning, why changes were made, and what still needs fixing.

---

## 1. What we observed

### 1.1 Audience (Matomo, last 7 days)

| Metric | Value | Note |
|---|---|---|
| Visits | 180 | Mostly generated in the last two days (tracking was only fully wired recently). |
| Actions / visit | 2.7 | People browse a few pages before leaving. |
| Bounce rate | 53% | Reasonable for cold traffic; room to improve. |
| Avg. time on site | 5 m 40 s | High intent when someone stays. |
| Top country | Germany (175 visits, 97%) | EU adset is driving almost all measurable traffic. |
| Other countries | Bulgaria (4), UK (1) | US adset is not yet delivering meaningful site volume. |
| Device split | Phablet 38%, Smartphone 36%, Desktop 18% | Audience is mobile-first. Creative and landing page must work on small screens. |
| Referrer | Campaigns 67%, Direct 27%, Websites 4%, Search 2% | Traffic is paid/retargeting driven; organic/search are still tiny. |
| Browser / app | Instagram, Facebook mobile | Confirms Meta placements are the current channel. |

**Audience hypothesis:** the current reachable audience is English-speaking, mobile-first founders and early-stage operators in Germany (and the broader EU adset), reached via Instagram/Facebook retargeting. They respond to control, speed, and sovereignty more than to abstract “shipped companies” messaging.

### 1.2 Creative performance (Meta, lifetime since launch)

| Ad ID | Variant | Status | Impressions | Clicks | CTR | CPC | Why it works / fails |
|---|---:|---|---:|---:|---:|---:|---|
| `120249350907820462` | EU V5 — “SAAS IS DEAD. SOVEREIGN AI IS BORN.” | ACTIVE | 11,886 | 433 | **3.64%** | **€0.060** | Strongest. Contrarian, local/on-desk ownership, clear enemy (SaaS/cloud). |
| `120249350237230462` | EU V4 — “Build a company without coding” | ACTIVE | 419 | 13 | 3.10% | €0.052 | Clear outcome + no-code + “you stay in control.” |
| `120249350230370462` | EU V2 — “YOUR AI CO-FOUNDER” | ACTIVE | 650 | 15 | 2.31% | €0.075 | Replaces the missing technical co-founder. |
| `120249350911340462` | EU V6 — “WHY RENT AI WHEN YOU CAN OWN THE FOUNDRY?” | ACTIVE | 9,901 | 192 | 1.94% | €0.145 | Same sovereignty theme as V5; slightly weaker CPC. |
| `120249350226320462` | EU V1 — Human co-founder | PAUSED | 1,875 | 17 | 0.91% | €0.234 | Too soft/generic; paused earlier. |
| `120249350233090462` | EU V3 — “IDEAS DON'T PAY. SHIPPED COMPANIES DO.” | **updated** | 149 | 0 | 0.00% | — | Failed. Abstract headline, no sovereignty/control hook. |
| `120249387437490462` | US V5 — “SAAS IS DEAD...” | ACTIVE | 389 | 36 | 9.25% | €0.089 | Tiny sample, but the same sovereignty copy wins. |
| `120249387441910462` | US V6 — “WHY RENT AI...” | ACTIVE | 1,714 | 146 | 8.52% | €0.090 | Same pattern as EU/US V5/V6. |
| `120249387428120462` | US V2 — “YOUR AI CO-FOUNDER” | ACTIVE | 35 | 4 | 11.43% | €0.038 | Very small sample. |
| `120249387433590462` | US V4 — “Build a company without coding” | ACTIVE | 4 | 1 | 25.00% | €0.020 | Tiny sample. |
| `120249387431010462` | US V3 — “IDEAS DON'T PAY...” | **updated** | n/a | 0 | — | — | No Meta data, but Matomo shows 8 landing visits from the old creative. |
| `120249387424560462` | US V1 — Human co-founder | ACTIVE | 15 | 1 | 6.67% | €0.050 | Tiny sample. |

**Key creative insight:** the winning proposition is **sovereignty + local ownership** (“your desk, not a cloud provider”, “own the foundry”). The losing proposition is **process/velocity** framed as “stop writing specs / shipped companies” without the sovereignty hook.

### 1.3 On-site behavior by creative (Matomo landing pages, last 7 days)

| utm_content (Ad ID) | Ad | Matomo visits | Matomo hits |
|---|---|---:|---:|
| `120249387441910462` | US V6 | 47 | 97 |
| `120249350907820462` | EU V5 | 45 | 84 |
| `120249387437490462` | US V5 | 24 | 46 |
| `120249350911340462` | EU V6 | 20 | 27 |
| `120249387431010462` | US V3 (old) | 8 | 28 |
| `120249387428120462` | US V2 | 5 | 6 |
| `120249350233090462` | EU V3 (old) | 2 | 3 |
| `120249387424560462` | US V1 | 1 | 1 |

**Observation:** Matomo confirms the same winner — V5/V6 creatives drive the most landing sessions. The old V3 creatives produced almost no on-site traffic.

### 1.4 Conversion signals

Matomo events, last 7 days:
- `conversion - initiate-checkout`: 24 events
- `conversion - lead`: 7 events

These are server-side events fired from `fabiaweb_shop`. No Meta Pixel conversion API events are visible in Matomo because we are not yet sending Pixel leads server-side as conversions.

---

## 2. Why we made the changes

| Change | Motivation |
|---|---|
| **Server-side Matomo tracking on both sites** | Meta gives ad-level clicks; Matomo gives real on-site behavior by ad creative. We need both to know which ad actually drives engagement. |
| **Async fire-and-forget tracking** | Matomo + Pixel calls must not block HTTP responses. Used `ThreadPoolExecutor` to mirror the existing Meta CAPI pattern. |
| **`ProxyFix` on Flask apps** | Both sites sit behind nginx. Without `ProxyFix`, Flask sees `127.0.0.1` and `http://localhost/`, so Matomo records the wrong IP/URL. |
| **Send `token_auth` via POST body** | Matomo 5 ignores `token_auth` in the query string for tracking hits. POST-ing it is required to forward the real client IP via `cip`. |
| **Hash-email `uid` for Matomo** | Lets us stitch sessions without exposing PII. Useful when a lead returns. |
| **Track PDF downloads and form errors** | Surface funnel drop-offs (e.g. missing email) that raw page views hide. |
| **Exclude internal IP + skip tracking in tests** | Stops our own traffic and test runs from polluting analytics. |
| **Versioned `/health` endpoints** | We need an uncached way to verify which git commit is actually deployed. |
| **Cache-control on `/health`** | Prevents CDN/browser from serving stale version JSON. |
| **Request + tracking logs** | Production `.env` issues are invisible without logs; now gunicorn prints every request and every Matomo/Pixel send/response. |
| **Unified favicon + correct `.ico` MIME type** | Both sites must look like the same brand. |
| **Rewrite Ad V3** | 0% CTR and almost no landing traffic. The creative angle was the weakest in the account, so we rebuilt it around the proven sovereignty + ship-fast hook. |

---

## 3. Actions taken

### 3.1 Infrastructure / tracking
- Added `matomo_tracker.py` to `fabia_web` and `fabiaweb_shop`.
- Copied canonical `meta_pixel.py` from `fabiaweb_shop` to `fabia_web` to unify the async Pixel implementation.
- Instrumented `server.py` in both apps with `track_page_view`, `track_event`, `track_download`, and form-error events.
- Added `ProxyFix`, hashed-email `uid`, internal-IP exclusion, and POST-body `token_auth`.
- Added `generate_version.py` and `/health` endpoints with cache-busting headers.
- Added request + Matomo + Pixel console logs.
- Updated `start.sh` / `deploy.sh` to regenerate `version.json` and include new files.
- Updated tests to pass and to skip tracking during `app.testing`.

### 3.2 Documentation / code templates
- Added `matomo_insights.py` reporting client to `fabiaweb_marketing`.
- Updated `docs/agents/Meta.md` to reflect the new Ad V3 angle.
- Updated `scripts/agentic_loop/content_agent.py` `_variant_speed()` so future generated variants use the winning sovereignty + ship-fast copy.

### 3.3 Live ad update (2026-07-10)
- Created new Ad V3 creatives for both EU and US adsets.
- New copy:
  - **Headline:** `OWN YOUR AI. SHIP YOUR COMPANY.`
  - **Primary text:** *“You have the idea. Fabia turns it into a launched product and business — without a dev team, without cloud lock-in, and without giving away your data. Approve the plan and ship from the box on your desk.”*
- Reused the winning V5 image hash (`6fdc8f0b5df6eea893dbcfac00a79b07`).
- Updated ad names to `... Ad V3 (Own the stack — ship fast)` and set status to `ACTIVE`.
- Ad IDs: `120249350233090462` (EU), `120249387431010462` (US). Currently showing `IN_PROCESS` while Meta reviews.

---

## 4. How it is going so far (2026-07-10 status check)

### 4.1 Meta account
- Account: ACTIVE, €41.33 lifetime spend.
- Campaign: `FABIABox — Website Retargeting`, ACTIVE, `OUTCOME_TRAFFIC`.
- 12 ads, 9 active + 2 new V3 in review.
- Winning angle is validated: V5/V6 lead in both EU and US adsets.

### 4.2 Websites / deployment
- `/health` on both sites returns JSON with git commit and deployed-at timestamp.
- Deployed commits:
  - `fabiabox.com`: `1de6ff27...` (pre-cache-control deployment).
  - `shop.fabiabox.com`: `69214a88...` (pre-cache-control deployment).
- **Cache-Control header is NOT yet live** — it was committed/pushed but not redeployed because SSH access to the production server is currently blocked.

### 4.3 Matomo tracking quality
- Matomo is receiving traffic and can segment by ad creative via `utm_content`.
- **Still recording server IP `159.223.27.54` for live visits.** This means the production `.env` files on the server are missing `MATOMO_TOKEN_AUTH` (or the apps have not been restarted since it was added). The manual curl test proved that when a valid token is sent via POST, Matomo records the real client IP.
- Germany is dominating traffic; real client location data is reliable once the token issue is fixed.

### 4.4 Conversions
- Server-side Matomo events are firing: 24 initiate-checkout, 7 lead events in the last 7 days.
- No Meta Pixel `Lead` conversion events are visible yet because the Pixel integration is click/page-view only; CAPI lead events are not wired to Meta conversions.

---

## 5. What is still blocked / next steps

| Blocker | Why it matters | Next action |
|---|---|---|
| SSH key `~/.ssh/hermes-agent` missing | Cannot redeploy apps, add production `MATOMO_TOKEN_AUTH`, or restart services. | Restore SSH access or run deploy manually on the server. |
| Production `.env` missing `MATOMO_TOKEN_AUTH` | Matomo records server IP instead of real client IP; tracking quality is degraded. | Add token to `.env` in both project dirs and restart gunicorn. |
| Production `.env` missing `MATOMO_EXCLUDE_IPS=78.83.114.98` | Internal traffic still counted. | Add the line and restart. |
| Cache-Control on `/health` not deployed | Version JSON may be cached by CDN. | Redeploy after SSH is restored. |
| Meta Pixel lead conversions not sent to Meta | Campaign cannot optimize for leads. | Wire server-side `Lead` event to Meta CAPI and create a `Lead` campaign only after ~50 leads/week per adset. |

### 5.1 Immediate tests once deploy is possible
1. Visit site from a non-excluded IP and confirm Matomo records the real client IP.
2. Confirm `/health` response includes `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`.
3. Let the new V3 creatives reach ~1,000 impressions, then compare CTR/CPC against V5/V6.

---

## 6. Creative recommendation summary

The account has found a working message:

> **Own your AI. Build it locally. Ship your company without a dev team or cloud lock-in.**

All future creative refreshes should:
1. Lead with **ownership / sovereignty** (not speed or process).
2. Include a concrete outcome (“live product and business”).
3. Call out the enemy: cloud providers, SaaS lock-in, or the missing technical co-founder.
4. Keep CTAs as `Learn More` while the objective remains `OUTCOME_TRAFFIC`; switch to `Sign Up` / `Get Offer` only after a dedicated lead-optimization campaign is viable.

Ad V3 was rebuilt to match this pattern. The next creative batch should be variations on “own the stack,” not new abstractions.
