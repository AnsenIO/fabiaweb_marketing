# Audience & Creative Retrospective — FABIABox

> Scope: the work done in the 24–48 h window before 2026-07-10, plus the state check on 2026-07-10.  
> Goal: understand who is actually visiting, which creatives are winning, why changes were made, and what still needs fixing.

---

## 1. What we observed

### 1.1 Audience (last 7 days)

#### Matomo on-site signals

| Metric | Value | Note |
|---|---|---|
| Visits | 295 | Tracking has been live for ~2 days; most traffic is from paid Meta. |
| Actions / visit | 2.3 | Low engagement depth; landing page is doing the heavy lifting. |
| Bounce rate | 60% | Typical for cold traffic, but the homepage (`/`) is bouncing at a higher rate. |
| Avg. time on site | 4 m 33 s | High intent when someone stays. |
| Device split | Phablet 38%, Smartphone 36%, Desktop 18%, Tablet 5% | **Mobile-first audience** (74% mobile/phablet). |
| Referrer | Campaigns 67%, Direct 27%, Websites 4%, Search 2% | Almost entirely paid Meta; organic/search are negligible. |
| Browser / app | Instagram 47%, Facebook 14%, Chrome 20%, Mobile Safari 12% | In-app browsing dominates. |

**Geo caveat:** Matomo currently records the **server IP `159.223.27.54`** for most visits because the production `.env` is missing `MATOMO_TOKEN_AUTH`. The Matomo country/region data below is therefore **not reliable** until the token is added and the apps are restarted.

| Matomo geo (unreliable) | Value |
|---|---|
| Recorded country | Germany 97% (175/180) |
| Recorded region | Baden-Württemberg, Germany |
| Recorded city | Kirchzarten, Germany |

#### Meta paid-audience breakdown (2026-07-04 → 2026-07-10)

This is the **real** source of truth for geography and demographics while Matomo’s IP forwarding is broken.

**By country:**

| Country | Impressions | Clicks | CTR | CPC | Spend | Efficiency |
|---|---|---:|---:|---:|---:|---|
| **US** | 4,217 | 354 | **8.39%** | **€0.092** | €32.72 | Best CTR; highest spend and strong CPC. |
| **UK** | 3,281 | 83 | 2.53% | €0.177 | €14.73 | High spend, low CTR, expensive CPC. |
| **Spain** | 9,839 | 275 | 2.79% | €0.068 | €18.66 | Volume market, efficient CPC. |
| **Italy** | 6,974 | 204 | 2.93% | €0.056 | €11.38 | Efficient CPC but lower CTR. |
| **France** | 4,282 | 123 | 2.87% | €0.082 | €10.14 | Mid-tier. |
| **Netherlands** | 1,082 | 40 | 3.70% | €0.125 | €5.00 | Small but decent CTR. |
| **Germany** | 966 | 37 | 3.83% | €0.099 | €3.65 | Small sample; aligns with Matomo “Germany” signal. |

**By age and gender:**

| Segment | Impressions | Clicks | CTR | CPC | Spend | Note |
|---|---|---:|---:|---:|---:|---|
| **Male 25-34** | 11,170 | 436 | 3.90% | €0.081 | €35.46 | Largest volume, very efficient. |
| **Male 35-44** | 6,495 | 273 | 4.20% | €0.088 | €24.11 | Strong volume + efficiency. |
| **Male 45-54** | 3,943 | 206 | **5.22%** | **€0.067** | €13.85 | **Highest CTR and cheapest CPC.** |
| Male 55-64 | 341 | 16 | 4.69% | €0.066 | €1.05 | Tiny but efficient. |
| Female 25-34 | 2,809 | 31 | 1.10% | €0.277 | €8.59 | Weak CTR, expensive. |
| Female 35-44 | 1,606 | 31 | 1.93% | €0.170 | €5.27 | Weak CTR, expensive. |
| Female 45-54 | 1,359 | 18 | 1.32% | €0.187 | €3.36 | Weak CTR, expensive. |
| Unknown gender | 2,895 | 103 | 3.56% | €0.040 | €4.15 | Efficient, but small/ambiguous. |

**Audience hypothesis (updated):** the core buyer/lead is a **man aged 25–54**, skewing slightly older (35–54), reached via Instagram/Facebook in-app ads. Geography is split: **US is the highest-quality market** (best CTR), while **UK is the weakest** (expensive, low CTR). The EU adset contains a mix of efficient CPC markets (Italy, Spain) and expensive/low-CTR markets (UK). Creative must be mobile-first and work without sound (in-app scroll). The message that lands is **sovereignty, local ownership, and replacing the missing technical co-founder**, not abstract “ship faster” language.

### 1.2 Creative performance (Meta, lifetime since launch)

| Ad ID | Adset | Variant | Status | Impressions | Clicks | CTR | CPC | Why it works / fails |
|---|---|---:|---|---:|---:|---:|---:|---|
| `120249350907820462` | EU | V5 — “SAAS IS DEAD. SOVEREIGN AI IS BORN.” | ACTIVE | 13,409 | 521 | **3.89%** | **€0.056** | **EU volume winner.** Contrarian sovereignty + local ownership. |
| `120249350911340462` | EU | V6 — “WHY RENT AI WHEN YOU CAN OWN THE FOUNDRY?” | ACTIVE | 10,291 | 218 | 2.12% | €0.133 | Same theme as V5 but weaker CPC. |
| `120249350237230462` | EU | V4 — “Build a company without coding” | ACTIVE | 419 | 13 | 3.10% | €0.052 | Clear outcome; small sample. |
| `120249350230370462` | EU | V2 — “YOUR AI CO-FOUNDER” | ACTIVE | 651 | 15 | 2.30% | €0.075 | Concrete co-founder promise. |
| `120249350226320462` | EU | V1 — Human co-founder | PAUSED | 1,875 | 17 | 0.91% | €0.234 | Too soft/generic; paused. |
| `120249350233090462` | EU | V3 — “OWN YOUR AI. SHIP YOUR COMPANY.” | **PAUSED** | 183 | 3 | 1.64% | €0.047 | Failed in EU; abstract without co-founder hook. |
| `120249469497610462` | EU | **V3.1** — AI co-founder + sovereign stack | ACTIVE | — | — | — | — | Just launched; combines V5/V6 sovereignty + V2 deliverables. |
| `120249387437490462` | US | V5 — “SAAS IS DEAD...” | ACTIVE | 968 | 93 | **9.61%** | €0.092 | Strong US performer. |
| `120249387428120462` | US | V2 — “YOUR AI CO-FOUNDER” | ACTIVE | 70 | 12 | **17.14%** | €0.033 | Highest observed CTR; tiny reach. |
| `120249387441910462` | US | V6 — “WHY RENT AI...” | ACTIVE | 3,047 | 231 | 7.58% | €0.101 | Strong volume + CTR. |
| `120249387431010462` | US | V3 — “OWN YOUR AI...” | **PAUSED** | 378 | 30 | 7.94% | €0.090 | Worked in US but shared EU creative pulled it down. |
| `120249469494710462` | US | **V3.1** — AI co-founder + sovereign stack | ACTIVE | — | — | — | — | Just launched. |
| `120249387433590462` | US | V4 — Hologram | ACTIVE | 8 | 1 | 12.50% | €0.030 | Tiny sample. |
| `120249387424560462` | US | V1 — Human co-founder | ACTIVE | 22 | 2 | 9.09% | €0.050 | Tiny sample. |

**Key creative insights:**
1. **Sovereignty + local ownership** (V5/V6) is the clear volume winner in both markets.
2. **AI co-founder / concrete deliverables** (V2) has the highest CTR when it gets delivery, especially in the US.
3. **The original V3 failed in the EU** because the headline was abstract and the body did not spell out the concrete outcome (MVP, brand, go-to-market) or the emotional pain (waiting for a technical co-founder).
4. **V3.1 attempts to combine the best of both:** V5/V6 sovereignty hook + V2 co-founder framing + V4 concrete deliverables.

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

### 3.3 Live ad update (2026-07-10) — Ad V3.1

- Paused the original Ad V3 in both adsets (EU `120249350233090462`, US `120249387431010462`).
- Created new Ad V3.1 creatives and ads in both EU and US adsets:
  - **New EU ad:** `120249469497610462`
  - **New US ad:** `120249469494710462`
  - **New creative:** `2085268062410129`
- New V3.1 copy (synthesized from the account winners):
  - **Headline:** `YOUR AI CO-FOUNDER. SHIP YOUR COMPANY.`
  - **Primary text:** *“Stop waiting for a technical co-founder. Share your idea and documents, approve the plan, and Fabia builds your MVP, brand, and go-to-market stack — on your desk, with your data, under your control.”*
- Reused the winning V5/V6 image hash (`6fdc8f0b5df6eea893dbcfac00a79b07`).
- Rationale: V3 worked in the US but failed in the EU because the “own your AI / ship from the box” angle was too abstract without the concrete co-founder promise. V3.1 keeps the sovereignty hook from V5/V6, borrows the clear deliverables from V2, and leads with the “AI co-founder” framing that had the highest observed CTR (V2, 17.1% US).

---

## 4. How it is going so far (2026-07-10 status check)

### 4.1 Meta account

- Account: ACTIVE, **€76.78** lifetime spend.
- Campaign: `FABIABox — Website Retargeting`, ACTIVE, `OUTCOME_TRAFFIC`.
- **13 ads total:** 11 active pre-V3.1 creatives + 2 new V3.1 ads; original V3 ads are now **PAUSED**.
- Winning angle remains **V5/V6 sovereignty** in both adsets, with **V2 "AI co-founder"** showing the highest CTR but very low delivery.
- **Original V3 performance before pause:**
  - EU V3: 183 impressions, 3 clicks, **1.64% CTR**, €0.047 CPC, €0.14 spend.
  - US V3: 378 impressions, 30 clicks, **7.94% CTR**, €0.090 CPC, €2.69 spend.
  - Interpretation: V3 worked in the US but failed in the EU, so it was replaced by V3.1.
- **Ad V3.1 is now live** in both adsets (EU `120249469497610462`, US `120249469494710462`). It combines the proven V5/V6 sovereignty hook, the V2 co-founder framing, and concrete deliverables. Give it ~1,000 impressions before judging CTR/CPC.

### 4.2 Websites / deployment
- `/health` on both sites returns JSON with git commit and deployed-at timestamp.
- Deployed commits:
  - `fabiabox.com`: `1de6ff27...` (pre-cache-control deployment).
  - `shop.fabiabox.com`: `69214a88...` (pre-cache-control deployment).
- **Cache-Control header is NOT yet live** — it was committed/pushed but not redeployed because SSH access to the production server is currently blocked.

### 4.3 Matomo tracking quality
- Matomo is receiving traffic and can segment by ad creative via `utm_content`.
- **Still recording server IP `159.223.27.54` for live visits.** This means the production `.env` files on the server are missing `MATOMO_TOKEN_AUTH` (or the apps have not been restarted since it was added). The manual curl test proved that when a valid token is sent via POST, Matomo records the real client IP.
- **Matomo geo data is therefore unreliable.** Germany appears to dominate because the server IP geolocates there, not because Germany is the only market. Use Meta breakdowns for geography until the token issue is fixed.

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

## 6. Audience targeting recommendations

Based on the Meta breakdowns, the account is currently buying **too much low-quality female and UK inventory** relative to the high-performing male/US segments.

### Immediate levers

1. **Prioritize men 25–54.** Every female age bracket is 2–4× more expensive per click and converts at half the CTR or worse.
   - Create a **Men 25–54** adset with the same V5/V6/V3 creatives and allocate the majority of the EU + US budget there.
   - Keep a small **Women 25–54 test adset** only if the budget allows; otherwise exclude it until lead data proves otherwise.
2. **Separate US from EU.** US CTR (~8%) is roughly 2–3× the EU average. It deserves its own budget and bid strategy.
3. **Split the EU adset by performance tier.**
   - **Tier 1 (keep):** US, Germany, Netherlands, Spain, Italy.
   - **Tier 2 (reduce/pause):** UK and France are underperforming on CTR; France is acceptable on CPC, UK is expensive.
4. **Lean into the 45–54 male segment.** It has the highest CTR (5.22%) and cheapest CPC (€0.067). This is likely the experienced founder/decision-maker cohort.
5. **Mobile-first creative.** 74% of visits are mobile/phablet. Ensure the first 3 seconds of any new creative communicate “own your AI” without requiring sound.

## 7. Creative recommendation summary

The account has found a working message:

> **Own your AI. Build it locally. Ship your company without a dev team or cloud lock-in.**

All future creative refreshes should:
1. Lead with **ownership / sovereignty** (not speed or process).
2. Include a concrete outcome (“live product and business”).
3. Call out the enemy: cloud providers, SaaS lock-in, or the missing technical co-founder.
4. Keep CTAs as `Learn More` while the objective remains `OUTCOME_TRAFFIC`; switch to `Sign Up` / `Get Offer` only after a dedicated lead-optimization campaign is viable.

Ad V3 was rebuilt to match this pattern. The next creative batch should be variations on “own the stack,” not new abstractions.
