#!/usr/bin/env python3
"""Exchange or refresh a Meta User Access Token and fetch a Page Access Token.

Meta token lifetimes (from https://developers.facebook.com/documentation/facebook-login/guides/access-tokens):
- Short-lived User Access Token: ~1-2 hours.
- Long-lived User Access Token: ~60 days. Can be refreshed by exchanging again before expiry.
- Page Access Token: does not expire when generated from a long-lived User Access Token.

Usage:
    python scripts/get_meta_long_lived_token.py <token_or_file>
    python scripts/get_meta_long_lived_token.py --refresh
"""
import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_URL = "https://graph.facebook.com/v19.0"


def load_env(repo_root: Path):
    load_dotenv(repo_root / "config" / ".env")
    return {
        "app_id": os.getenv("META_APP_ID", "").strip(),
        "app_secret": os.getenv("META_APP_SECRET", "").strip(),
        "page_id": os.getenv("META_PAGE_ID", "").strip(),
        "access_token": os.getenv("META_ACCESS_TOKEN", "").strip(),
    }


def exchange_token(app_id: str, app_secret: str, short_token: str) -> dict:
    url = f"{BASE_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }

    masked = f"{short_token[:8]}...{short_token[-8:]}"
    print(f"GET {url}")
    print(f"  grant_type=fb_exchange_token")
    print(f"  client_id={app_id}")
    print(f"  client_secret=***")
    print(f"  fb_exchange_token={masked}")

    resp = requests.get(url, params=params, timeout=60)
    data = resp.json()
    if resp.status_code >= 400 or "error" in data:
        raise RuntimeError(f"Meta token exchange error: {data.get('error', data)}")
    return data


def fetch_page_token(user_token: str, page_id: str) -> str:
    url = f"{BASE_URL}/me/accounts"
    params = {"access_token": user_token, "fields": "id,name,access_token"}
    resp = requests.get(url, params=params, timeout=60)
    data = resp.json()
    if resp.status_code >= 400 or "error" in data:
        raise RuntimeError(f"Page token fetch error: {data.get('error', data)}")
    for account in data.get("data", []):
        if account["id"] == page_id:
            return account["access_token"]
    raise RuntimeError(f"Page {page_id} not found in /me/accounts")


def update_env(env_path: Path, key: str, value: str):
    if env_path.exists():
        text = env_path.read_text()
    else:
        text = ""
    pattern = re.compile(rf"^{re.escape(key)}=.*$", flags=re.MULTILINE)
    if pattern.search(text):
        text = pattern.sub(f"{key}={value}", text)
    else:
        text += f"\n{key}={value}\n"
    env_path.write_text(text)


def save_expiry(repo_root: Path, seconds: int):
    expiry = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    path = repo_root / "config" / "meta_token_expiry.txt"
    path.write_text(expiry.isoformat())
    print(f"   Expiry saved to {path}")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    env = load_env(repo_root)
    env_path = repo_root / "config" / ".env"

    if not env["app_id"] or not env["app_secret"]:
        print("Error: META_APP_ID and META_APP_SECRET must be set in config/.env")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Exchange/refresh Meta long-lived access token and page token."
    )
    parser.add_argument(
        "token_or_file",
        nargs="?",
        help="Short-lived token string or path to a file containing it",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh the existing META_ACCESS_TOKEN before it expires",
    )
    args = parser.parse_args()

    if args.refresh:
        if not env["access_token"]:
            print("Error: no META_ACCESS_TOKEN to refresh")
            sys.exit(1)
        token_to_exchange = env["access_token"]
        print("Refreshing existing long-lived token...")
    elif args.token_or_file:
        token_arg = args.token_or_file
        token_file = Path(token_arg)
        try:
            is_file = token_file.exists()
        except OSError:
            is_file = False
        if is_file:
            token_to_exchange = token_file.read_text().strip()
        else:
            token_to_exchange = token_arg.strip()
        if not token_to_exchange:
            print("Error: token is empty")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    data = exchange_token(env["app_id"], env["app_secret"], token_to_exchange)
    long_token = data.get("access_token")
    expires_in = data.get("expires_in")

    if not long_token:
        print(f"Unexpected response: {data}")
        sys.exit(1)

    update_env(env_path, "META_ACCESS_TOKEN", long_token)
    print("✅ Updated META_ACCESS_TOKEN")
    if expires_in:
        print(f"   Expires in: {expires_in} seconds (~{expires_in // 86400} days)")
        save_expiry(repo_root, int(expires_in))

    if env["page_id"]:
        try:
            page_token = fetch_page_token(long_token, env["page_id"])
            update_env(env_path, "META_PAGE_ACCESS_TOKEN", page_token)
            print("✅ Updated META_PAGE_ACCESS_TOKEN")
        except Exception as exc:
            print(f"⚠️ Could not update page token: {exc}")
    else:
        print("⚠️ META_PAGE_ID not set; skipping page token update")

    masked = f"{long_token[:8]}...{long_token[-8:]}"
    print(f"   Masked token: {masked}")


if __name__ == "__main__":
    main()
