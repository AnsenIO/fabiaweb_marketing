#!/usr/bin/env python3
"""Final closing statistics for Meta marketing on the FABIABox project.

Pulls lifetime insights at campaign, adset, and ad level plus audience
breakdowns (country, age, gender), and prints a consolidated report.
"""

import hashlib
import hmac
import json
import os
import sys
import time
from collections import defaultdict

import requests
from dotenv import load_dotenv

API_VERSION = "v19.0"


def load_config():
    env_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")
    load_dotenv(env_path)
    account = os.getenv("META_AD_ACCOUNT_ID") or ""
    cfg = {
        "app_secret": os.getenv("META_APP_SECRET"),
        "access_token": os.getenv("META_ACCESS_TOKEN"),
        "ad_account_id": account.lstrip("act_"),
    }
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        print(f"Missing config keys: {missing}")
        sys.exit(1)
    return cfg


def proof(cfg):
    return hmac.new(
        cfg["app_secret"].encode(), cfg["access_token"].encode(), hashlib.sha256
    ).hexdigest()


def api_get(cfg, path, params=None, retries=4):
    p = params or {}
    p["access_token"] = cfg["access_token"]
    p["appsecret_proof"] = proof(cfg)
    url = f"https://graph.facebook.com/{API_VERSION}/{path}"
    for attempt in range(retries):
        try:
            r = requests.get(url, params=p, timeout=60)
            data = r.json()
            if r.status_code == 200:
                return data
            err = data.get("error", {})
            if err.get("code") in (17, 4, 32) or err.get("is_transient"):
                wait = 2 ** attempt * 2
                print(f"  rate-limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            raise RuntimeError(f"Meta API error: {err}")
        except requests.RequestException as e:
            wait = 2 ** attempt * 2
            print(f"  network error ({e}), waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"Failed after {retries} retries: {path}")


def f2(x):
    """Format a number to 2 decimals."""
    try:
        return f"{float(x):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def lpv_of(row):
    """Extract landing-page-view count from actions list."""
    for a in row.get("actions") or []:
        if a.get("action_type") == "landing_page_view":
            return int(a.get("value", 0))
    return 0


def main():
    cfg = load_config()
    acct = cfg["ad_account_id"]

    # ---------- Account-level lifetime ----------
    print("Fetching account lifetime insights...")
    acct_ins = api_get(cfg, f"act_{acct}/insights", params={
        "fields": "spend,impressions,clicks,reach,cpc,ctr",
        "date_preset": "maximum",
    })
    acct_row = (acct_ins.get("data") or [{}])[0]

    # ---------- Campaign level ----------
    print("Fetching campaign insights...")
    camp_ins = api_get(cfg, f"act_{acct}/insights", params={
        "level": "campaign",
        "fields": "campaign_id,campaign_name,spend,impressions,clicks,reach,ctr,cpc,actions",
        "date_preset": "maximum",
        "limit": 100,
    })
    campaigns = camp_ins.get("data", [])

    # ---------- Adset level ----------
    print("Fetching adset insights...")
    adset_ins = api_get(cfg, f"act_{acct}/insights", params={
        "level": "adset",
        "fields": "adset_id,adset_name,spend,impressions,clicks,reach,ctr,cpc,actions",
        "date_preset": "maximum",
        "limit": 100,
    })
    adsets = adset_ins.get("data", [])

    # ---------- Ad level ----------
    print("Fetching ad-level insights...")
    ad_ins = api_get(cfg, f"act_{acct}/insights", params={
        "level": "ad",
        "fields": "ad_id,ad_name,adset_id,adset_name,spend,impressions,clicks,reach,ctr,cpc,actions",
        "date_preset": "maximum",
        "limit": 200,
    })
    ads = ad_ins.get("data", [])

    # ---------- Breakdowns ----------
    breakdowns = {}
    for b in ("country", "age", "gender"):
        print(f"Fetching breakdown: {b}...")
        try:
            r = api_get(cfg, f"act_{acct}/insights", params={
                "level": "account",
                "fields": "spend,impressions,clicks,actions",
                "breakdowns": b,
                "date_preset": "maximum",
                "limit": 200,
            })
            breakdowns[b] = r.get("data", [])
        except Exception as e:
            print(f"  (skipped {b}: {e})")
            breakdowns[b] = []
        time.sleep(0.5)

    # ================= REPORT =================
    report = []

    report.append("# FABIABox Meta Marketing — Final Closing Statistics")
    report.append("")
    report.append(f"Reporting window: maximum lifetime (all time)")
    report.append("")
    report.append("## 1. Account totals")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|---|---|")
    report.append(f"| Total spend | €{f2(acct_row.get('spend'))} |")
    report.append(f"| Impressions | {int(float(acct_row.get('impressions', 0) or 0)):,} |")
    report.append(f"| Clicks | {int(float(acct_row.get('clicks', 0) or 0)):,} |")
    report.append(f"| Reach | {int(float(acct_row.get('reach', 0) or 0)):,} |")
    report.append(f"| Avg CTR | {f2(acct_row.get('ctr'))}% |")
    report.append(f"| Avg CPC | €{f2(acct_row.get('cpc'))} |")
    report.append("")

    # campaigns
    report.append("## 2. Campaign performance")
    report.append("")
    report.append("| Campaign | Spend | Impressions | Clicks | CTR | CPC | LPV | €/LPV |")
    report.append("|---|---|---|---|---|---|---|---|")
    for c in sorted(campaigns, key=lambda x: -float(x.get("spend", 0) or 0)):
        lpv = lpv_of(c)
        spend = float(c.get("spend", 0) or 0)
        e_lpv = f"€{f2(spend/lpv)}" if lpv else "—"
        report.append(
            f"| {c.get('campaign_name','?')} | €{f2(spend)} | "
            f"{int(float(c.get('impressions',0) or 0)):,} | "
            f"{int(float(c.get('clicks',0) or 0)):,} | {f2(c.get('ctr'))}% | "
            f"€{f2(c.get('cpc'))} | {lpv:,} | {e_lpv} |"
        )
    report.append("")

    # adsets
    report.append("## 3. Adset performance")
    report.append("")
    report.append("| Adset | Spend | Impressions | Clicks | CTR | CPC | LPV | €/LPV |")
    report.append("|---|---|---|---|---|---|---|---|")
    for s in sorted(adsets, key=lambda x: -float(x.get("spend", 0) or 0)):
        lpv = lpv_of(s)
        spend = float(s.get("spend", 0) or 0)
        e_lpv = f"€{f2(spend/lpv)}" if lpv else "—"
        report.append(
            f"| {s.get('adset_name','?')} | €{f2(spend)} | "
            f"{int(float(s.get('impressions',0) or 0)):,} | "
            f"{int(float(s.get('clicks',0) or 0)):,} | {f2(s.get('ctr'))}% | "
            f"€{f2(s.get('cpc'))} | {lpv:,} | {e_lpv} |"
        )
    report.append("")

    # ads
    report.append("## 4. Ad-level performance (all ads)")
    report.append("")
    report.append("| Ad | Adset | Spend | Impr. | Clicks | CTR | CPC | LPV | €/LPV |")
    report.append("|---|---|---|---|---|---|---|---|---|")
    for a in sorted(ads, key=lambda x: -float(x.get("spend", 0) or 0)):
        lpv = lpv_of(a)
        spend = float(a.get("spend", 0) or 0)
        e_lpv = f"€{f2(spend/lpv)}" if lpv else "—"
        name = (a.get("ad_name", "?")).replace("|", "\\|")
        aset = (a.get("adset_name", "?")).replace("|", "\\|")
        report.append(
            f"| {name} | {aset} | €{f2(spend)} | "
            f"{int(float(a.get('impressions',0) or 0)):,} | "
            f"{int(float(a.get('clicks',0) or 0)):,} | {f2(a.get('ctr'))}% | "
            f"€{f2(a.get('cpc'))} | {lpv:,} | {e_lpv} |"
        )
    report.append("")

    # breakdowns
    report.append("## 5. Audience breakdowns")
    for b in ("country", "age", "gender"):
        rows = breakdowns.get(b) or []
        if not rows:
            continue
        agg = defaultdict(lambda: {"spend": 0.0, "impr": 0, "clicks": 0, "lpv": 0})
        for r in rows:
            key = r.get(b, "?")
            agg[key]["spend"] += float(r.get("spend", 0) or 0)
            agg[key]["impr"] += int(float(r.get("impressions", 0) or 0))
            agg[key]["clicks"] += int(float(r.get("clicks", 0) or 0))
            agg[key]["lpv"] += lpv_of(r)
        report.append("")
        report.append(f"### By {b}")
        report.append("")
        report.append(f"| {b.title()} | Spend | Impr. | Clicks | CTR | CPC | €/LPV |")
        report.append("|---|---|---|---|---|---|---|")
        for key, v in sorted(agg.items(), key=lambda kv: -kv[1]["spend"]):
            if v["spend"] == 0 and v["impr"] == 0:
                continue
            ctr = (v["clicks"] / v["impr"] * 100) if v["impr"] else 0
            cpc = (v["spend"] / v["clicks"]) if v["clicks"] else 0
            elpv = f"€{f2(v['spend']/v['lpv'])}" if v["lpv"] else "—"
            report.append(
                f"| {key} | €{f2(v['spend'])} | {v['impr']:,} | {v['clicks']:,} | "
                f"{f2(ctr)}% | €{f2(cpc)} | {elpv} |"
            )
    report.append("")

    text = "\n".join(report)
    print(text)

    out_path = os.path.join(os.path.dirname(__file__), "..", "docs", "meta-final-stats-2026-07.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        fh.write(text + "\n")
    print(f"\nSaved report to {out_path}")


if __name__ == "__main__":
    main()
