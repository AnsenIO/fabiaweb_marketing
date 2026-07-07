import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


def load_config():
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / "config" / ".env")

    with open(repo_root / "config" / "marketing.yaml") as f:
        cfg = yaml.safe_load(f)

    # Override YAML with env vars where provided
    cfg["llm"]["base_url"] = os.getenv("OPENAI_BASE_URL", cfg["llm"].get("base_url"))
    cfg["llm"]["api_key"] = os.getenv("OPENAI_API_KEY", cfg["llm"].get("api_key"))

    for key, env_name in [
        ("mailtrain_url", "MAILTRAIN_URL"),
        ("mailtrain_api_key", "MAILTRAIN_API_KEY"),
        ("mailtrain_list_id", "MAILTRAIN_LIST_ID"),
    ]:
        cfg["channels"]["email"][key] = os.getenv(env_name, cfg["channels"]["email"].get(key, ""))

    cfg["channels"]["discord"]["webhook_url"] = os.getenv(
        "DISCORD_WEBHOOK_URL", cfg["channels"]["discord"].get("webhook_url", "")
    )

    cfg["channels"]["meta"]["ad_account_id"] = os.getenv(
        "META_AD_ACCOUNT_ID", cfg["channels"]["meta"].get("ad_account_id", "")
    )
    cfg["channels"]["meta"]["pixel_id"] = os.getenv(
        "META_PIXEL_ID", cfg["channels"]["meta"].get("pixel_id", "")
    )
    cfg["channels"]["meta"]["access_token"] = os.getenv(
        "META_ACCESS_TOKEN", cfg["channels"]["meta"].get("access_token", "")
    )

    return cfg
