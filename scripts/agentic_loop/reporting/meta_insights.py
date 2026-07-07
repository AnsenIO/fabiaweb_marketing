import hashlib
import hmac

import requests


API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


class MetaInsights:
    def __init__(self, cfg: dict):
        self.ad_account_id = cfg.get("ad_account_id", "").lstrip("act_")
        self.access_token = cfg.get("access_token", "")
        self.app_secret = cfg.get("app_secret", "")

    def _proof(self) -> str:
        if not self.app_secret or not self.access_token:
            return ""
        return hmac.new(
            self.app_secret.encode("utf-8"),
            self.access_token.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, path: str, params: dict | None = None) -> dict:
        url = f"{BASE_URL}/{path}"
        params = params or {}
        params["access_token"] = self.access_token
        proof = self._proof()
        if proof:
            params["appsecret_proof"] = proof
        resp = requests.get(url, params=params, timeout=60)
        data = resp.json()
        if resp.status_code >= 400 or "error" in data:
            raise RuntimeError(f"Meta API error: {data.get('error', data)}")
        return data

    def fetch(
        self,
        level: str = "ad",
        date_preset: str = "last_7d",
        fields: tuple[str, ...] = (
            "campaign_name",
            "adset_name",
            "ad_name",
            "impressions",
            "clicks",
            "ctr",
            "cpc",
            "spend",
            "reach",
            "frequency",
        ),
    ) -> list[dict]:
        path = f"act_{self.ad_account_id}/insights"
        params = {
            "level": level,
            "date_preset": date_preset,
            "fields": ",".join(fields),
        }
        result = self._request(path, params)
        return result.get("data", [])

    def print_report(self, rows: list[dict]) -> None:
        if not rows:
            print("No insights data yet.")
            return
        headers = ["Campaign", "AdSet", "Ad", "Impr", "Clicks", "CTR", "CPC", "Spend"]
        col_widths = [max(len(h), 18) for h in headers]
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * len(header_line))
        for row in rows:
            print(
                " | ".join(
                    str(row.get(k, ""))[:w].ljust(w)
                    for k, w in zip(
                        ["campaign_name", "adset_name", "ad_name", "impressions", "clicks", "ctr", "cpc", "spend"],
                        col_widths,
                    )
                )
            )
