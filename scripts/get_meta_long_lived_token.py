#!/usr/bin/env python3
"""Exchange a short-lived Meta User Access Token for a long-lived one.

Usage:
    python scripts/get_meta_long_lived_token.py /path/to/short_lived_token.txt
"""
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def main():
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root / "config" / ".env")

    app_id = os.getenv("META_APP_ID", "").strip()
    app_secret = os.getenv("META_APP_SECRET", "").strip()

    if not app_id or not app_secret:
        print("Error: META_APP_ID and META_APP_SECRET must be set in config/.env")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python scripts/get_meta_long_lived_token.py <path_to_short_token_file>")
        sys.exit(1)

    token_file = Path(sys.argv[1])
    if not token_file.exists():
        print(f"Error: token file not found: {token_file}")
        sys.exit(1)

    short_token = token_file.read_text().strip()
    if not short_token:
        print("Error: token file is empty")
        sys.exit(1)

    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }

    try:
        resp = requests.get(url, params=params, timeout=60)
        data = resp.json()
    except Exception as exc:
        print(f"Error exchanging token: {exc}")
        sys.exit(1)

    if "error" in data:
        print(f"Meta API error: {data['error']}")
        sys.exit(1)

    long_token = data.get("access_token")
    expires_in = data.get("expires_in")

    if not long_token:
        print(f"Unexpected response: {data}")
        sys.exit(1)

    env_path = repo_root / "config" / ".env"
    env_text = env_path.read_text()

    if re.search(r"^META_ACCESS_TOKEN=", env_text, flags=re.MULTILINE):
        env_text = re.sub(
            r"^META_ACCESS_TOKEN=.*$",
            f"META_ACCESS_TOKEN={long_token}",
            env_text,
            flags=re.MULTILINE,
        )
    else:
        env_text += f"\nMETA_ACCESS_TOKEN={long_token}\n"

    env_path.write_text(env_text)
    print("✅ Updated config/.env with long-lived Meta access token.")
    print(f"   Expires in: {expires_in} seconds (~{expires_in // 86400} days)")
    print(f"   Masked token: {long_token[:8]}...{long_token[-8:]}")


if __name__ == "__main__":
    main()
