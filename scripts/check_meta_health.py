#!/usr/bin/env python3
"""Quick Meta health check: campaigns, ads, page, spend."""
import sys
from datetime import datetime, timedelta

sys.path.insert(0, "scripts")

from agentic_loop.config import load_config
from agentic_loop.publishers.meta import MetaPublisher


def fmt_eur(value):
    if value is None or value == "":
        return "n/a"
    try:
        return f"€{float(value) / 100:,.2f}"
    except (TypeError, ValueError):
        return str(value)


def fmt_int(value):
    if value is None:
        return "n/a"
    return str(value)


def main():
    cfg = load_config()
    p = MetaPublisher(cfg["channels"]["meta"])

    print("== Meta health check ==\n")

    # Account
    try:
        account = p._request(
            "GET",
            f"act_{p.ad_account_id.lstrip('act_')}",
            params={"fields": "account_id,name,account_status,currency,timezone_name,spend_cap,amount_spent"},
        )
        status = account.get("account_status")
        status_label = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW", 9: "IN_GRACE_PERIOD", 100: "PENDING_CLOSURE", 101: "ANY_ACTIVE", 102: "ANY_CLOSED"}.get(status, status)
        print(f"Ad account: {account.get('name')} ({account.get('account_id')})")
        print(f"Status: {status_label}")
        print(f"Currency: {account.get('currency')}")
        print(f"Spend cap: {fmt_eur(account.get('spend_cap'))}")
        print(f"Amount spent: {fmt_eur(account.get('amount_spent'))}\n")
    except Exception as exc:
        print(f"Account check failed: {exc}\n")

    # Campaigns
    try:
        campaigns = p._request(
            "GET",
            f"act_{p.ad_account_id.lstrip('act_')}/campaigns",
            params={"fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,budget_remaining,insights.date_preset(maximum){spend,impressions,clicks,reach}", "limit": 50},
        )
        print(f"Campaigns: {len(campaigns.get('data', []))}")
        for c in campaigns.get("data", []):
            insights = (c.get("insights") or {}).get("data", [{}])[0]
            print(f"  - {c.get('name')} | status={c.get('effective_status')} | objective={c.get('objective')} | spend={fmt_eur(insights.get('spend'))} | impressions={fmt_int(insights.get('impressions'))} | clicks={fmt_int(insights.get('clicks'))}")
        print()
    except Exception as exc:
        print(f"Campaign check failed: {exc}\n")

    # Adsets / Ads
    try:
        ads = p._request(
            "GET",
            f"act_{p.ad_account_id.lstrip('act_')}/ads",
            params={"fields": "id,name,adset_id,campaign_id,status,effective_status,preview_shareable_link,insights.date_preset(maximum){spend,impressions,clicks,reach}", "limit": 100},
        )
        active_ads = [a for a in ads.get("data", []) if a.get("effective_status") == "ACTIVE"]
        print(f"Ads: {len(ads.get('data', []))} total, {len(active_ads)} active\n")
        for a in ads.get("data", []):
            insights = (a.get("insights") or {}).get("data", [{}])[0]
            print(f"  - {a.get('name')} | {a.get('effective_status')} | spend={fmt_eur(insights.get('spend'))} | impressions={fmt_int(insights.get('impressions'))} | clicks={fmt_int(insights.get('clicks'))}")
        print()
    except Exception as exc:
        print(f"Ads check failed: {exc}\n")

    # Page
    try:
        page = p._request("GET", p.page_id, params={"fields": "name,about,website,phone,description,company_overview,mission,general_info,fan_count"})
        print("Facebook page:")
        for field in ["name", "about", "website", "phone", "description", "company_overview", "mission", "general_info", "fan_count"]:
            print(f"  {field}: {page.get(field)}")
        print()
    except Exception as exc:
        print(f"Page check failed: {exc}\n")


if __name__ == "__main__":
    main()
