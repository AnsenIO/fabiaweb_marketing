#!/usr/bin/env python3
"""Pause all currently ACTIVE Meta campaigns for the configured ad account."""

import hashlib
import hmac
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv


def load_config():
    env_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")
    load_dotenv(env_path)
    cfg = {
        "app_id": os.getenv("META_APP_ID"),
        "app_secret": os.getenv("META_APP_SECRET"),
        "access_token": os.getenv("META_ACCESS_TOKEN"),
        "ad_account_id": os.getenv("META_AD_ACCOUNT_ID"),
    }
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        print(f"Missing config keys: {missing}")
        sys.exit(1)
    return cfg


def appsecret_proof(app_secret, access_token):
    return hmac.new(
        app_secret.encode("utf-8"),
        access_token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def api_get(cfg, path, params=None):
    url = f"https://graph.facebook.com/v19.0/{path}"
    p = params or {}
    p["access_token"] = cfg["access_token"]
    p["appsecret_proof"] = appsecret_proof(cfg["app_secret"], cfg["access_token"])
    r = requests.get(url, params=p, timeout=60)
    r.raise_for_status()
    return r.json()


def api_post(cfg, path, data=None):
    url = f"https://graph.facebook.com/v19.0/{path}"
    d = data or {}
    d["access_token"] = cfg["access_token"]
    d["appsecret_proof"] = appsecret_proof(cfg["app_secret"], cfg["access_token"])
    r = requests.post(url, data=d, timeout=60)
    r.raise_for_status()
    return r.json()


def list_active_campaigns(cfg):
    account_id = cfg["ad_account_id"].lstrip("act_")
    return api_get(
        cfg,
        f"act_{account_id}/campaigns",
        params={
            "fields": "id,name,status,effective_status,objective,spend",
            "effective_status": "['ACTIVE']",
            "limit": 100,
        },
    )


def pause_campaign(cfg, campaign_id):
    return api_post(cfg, campaign_id, data={"status": "PAUSED"})


def main():
    cfg = load_config()
    print("Fetching active campaigns...")
    resp = list_active_campaigns(cfg)
    campaigns = resp.get("data", [])
    if not campaigns:
        print("No ACTIVE campaigns found.")
        return

    print(f"Found {len(campaigns)} active campaign(s):")
    for c in campaigns:
        print(f"  - {c['name']} ({c['id']}) — spend €{c.get('spend', 'n/a')}")

    for c in campaigns:
        cid = c["id"]
        print(f"Pausing {cid} ({c['name']})...")
        try:
            result = pause_campaign(cfg, cid)
            print(f"  OK: {result}")
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(0.5)

    print("\nVerifying...")
    resp = list_active_campaigns(cfg)
    remaining = resp.get("data", [])
    if remaining:
        print(f"Still active: {len(remaining)}")
        for c in remaining:
            print(f"  - {c['name']} ({c['id']})")
    else:
        print("All campaigns paused.")


if __name__ == "__main__":
    main()
