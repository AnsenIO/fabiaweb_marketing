import hmac
import hashlib
import json

import requests

from .base import Publisher


API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


class MetaPublisher(Publisher):
    name = "meta"

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.ad_account_id = cfg.get("ad_account_id", "")
        self.access_token = cfg.get("access_token", "")
        self.app_secret = cfg.get("app_secret", "")
        self.pixel_id = cfg.get("pixel_id", "")
        self.page_id = cfg.get("page_id", "")
        self.status = cfg.get("ad_status", "PAUSED").upper()
        self.dsa = cfg.get("dsa", {}) or {}
        self.image_url = cfg.get("image_url", "")
        self.image_path = cfg.get("image_path", "")

    def _proof(self) -> str:
        if not self.app_secret or not self.access_token:
            return ""
        return hmac.new(
            self.app_secret.encode("utf-8"),
            self.access_token.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> dict:
        url = f"{BASE_URL}/{path}"
        params = params or {}
        params["access_token"] = self.access_token
        proof = self._proof()
        if proof:
            params["appsecret_proof"] = proof
        try:
            resp = requests.request(method, url, params=params, json=json_data, timeout=60)
            data = resp.json()
            if resp.status_code >= 400 or "error" in data:
                raise RuntimeError(f"Meta API error: {data.get('error', data)}")
            return data
        except requests.RequestException as exc:
            raise RuntimeError(f"Meta API request failed: {exc}") from exc

    def upload_image(self, image_path: str) -> str:
        if not image_path:
            raise RuntimeError("No image_path configured for Meta ad creative")
        path = f"act_{self.ad_account_id.lstrip('act_')}/adimages"
        url = f"{BASE_URL}/{path}"
        params = {"access_token": self.access_token}
        proof = self._proof()
        if proof:
            params["appsecret_proof"] = proof
        try:
            with open(image_path, "rb") as f:
                files = {"file": (image_path.split("/")[-1], f, "image/png")}
                resp = requests.post(url, params=params, files=files, timeout=120)
            data = resp.json()
            if resp.status_code >= 400 or "error" in data:
                raise RuntimeError(f"Meta API error: {data.get('error', data)}")
            images = data.get("images", {})
            if not images:
                raise RuntimeError(f"Unexpected image upload response: {data}")
            return next(iter(images.values())).get("hash")
        except requests.RequestException as exc:
            raise RuntimeError(f"Meta image upload failed: {exc}") from exc

    def validate(self) -> dict:
        if not self.access_token:
            raise RuntimeError("META_ACCESS_TOKEN is missing")
        if not self.ad_account_id:
            raise RuntimeError("META_AD_ACCOUNT_ID is missing")

        me = self._request("GET", "me", params={"fields": "id,name,email"})
        account = self._request(
            "GET",
            f"act_{self.ad_account_id.lstrip('act_')}",
            params={"fields": "account_id,name,account_status,currency,timezone_name"},
        )
        campaigns = self._request(
            "GET",
            f"act_{self.ad_account_id.lstrip('act_')}/campaigns",
            params={"limit": 1},
        )
        return {
            "user": me,
            "ad_account": account,
            "existing_campaigns": campaigns.get("data", []),
        }

    def create_campaign(self, name: str, objective: str) -> str:
        path = f"act_{self.ad_account_id.lstrip('act_')}/campaigns"
        payload = {
            "name": name,
            "objective": objective,
            "status": self.status,
            "special_ad_categories": [],
            "is_adset_budget_sharing_enabled": False,
        }
        result = self._request("POST", path, json_data=payload)
        return result["id"]

    def create_adset(
        self,
        campaign_id: str,
        name: str,
        daily_budget_eur: float,
        custom_audience_id: str | None = None,
        optimization_goal: str = "LINK_CLICKS",
        billing_event: str = "IMPRESSIONS",
    ) -> str:
        path = f"act_{self.ad_account_id.lstrip('act_')}/adsets"
        targeting = {
            "geo_locations": {"countries": ["FR", "DE", "GB", "ES", "IT", "NL"]},
            "age_min": 25,
            "age_max": 55,
            "targeting_automation": {"advantage_audience": 0},
        }
        if custom_audience_id:
            targeting["custom_audiences"] = [{"id": custom_audience_id}]

        payload = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": int(daily_budget_eur * 100),  # cents
            "billing_event": billing_event,
            "optimization_goal": optimization_goal,
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "targeting": json.dumps(targeting),
            "status": self.status,
        }
        if self.pixel_id:
            payload["promoted_object"] = json.dumps(
                {"pixel_id": self.pixel_id, "custom_event_type": "VIEW_CONTENT"}
            )

        if self.dsa.get("beneficiary"):
            payload["dsa_beneficiary"] = self.dsa["beneficiary"]
        if self.dsa.get("payor"):
            payload["dsa_payor"] = self.dsa["payor"]

        result = self._request("POST", path, json_data=payload)
        return result["id"]

    def create_adcreative(
        self,
        name: str,
        message: str,
        link: str,
        headline: str,
        image_hash: str,
        cta_type: str = "LEARN_MORE",
    ) -> str:
        if not self.page_id:
            raise RuntimeError("META_PAGE_ID is required to create ad creatives")

        allowed_ctas = {
            "LEARN_MORE", "SIGN_UP", "SHOP_NOW", "DOWNLOAD", "CONTACT_US",
            "BOOK_NOW", "GET_OFFER", "SUBSCRIBE", "APPLY_NOW", "GET_QUOTE",
            "BUY_NOW", "MESSAGE_PAGE", "WHATSAPP_MESSAGE", "GET_DIRECTIONS",
        }
        normalized_cta = cta_type.upper().replace(" ", "_")
        if normalized_cta not in allowed_ctas:
            normalized_cta = "LEARN_MORE"

        path = f"act_{self.ad_account_id.lstrip('act_')}/adcreatives"
        payload = {
            "name": name,
            "object_story_spec": json.dumps(
                {
                    "page_id": self.page_id,
                    "link_data": {
                        "message": message,
                        "link": link,
                        "name": headline,
                        "image_hash": image_hash,
                        "call_to_action": {"type": normalized_cta, "value": {"link": link}},
                    },
                }
            ),
        }
        result = self._request("POST", path, json_data=payload)
        return result["id"]

    def create_ad(self, adset_id: str, creative_id: str, name: str) -> str:
        path = f"act_{self.ad_account_id.lstrip('act_')}/ads"
        payload = {
            "name": name,
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": self.status,
        }
        result = self._request("POST", path, json_data=payload)
        return result["id"]

    def publish(self, content: str, metadata: dict) -> dict:
        if not self.ad_account_id or not self.access_token:
            return {"status": "skipped", "reason": "missing Meta ad account or access token"}

        if not self.page_id:
            return {"status": "skipped", "reason": "missing META_PAGE_ID"}

        campaign_cfg = self.cfg.get("campaigns", {}).get("retargeting_website", {})
        campaign_name = campaign_cfg.get("name", "FABIABox — Website Retargeting")
        objective = campaign_cfg.get("objective", "OUTCOME_TRAFFIC")
        daily_budget = campaign_cfg.get("daily_budget_eur", 20)

        # Parse creative JSON if provided; otherwise use defaults
        try:
            creative = json.loads(content)
        except json.JSONDecodeError:
            creative = {
                "headline": "Ship your company with AI",
                "primary_text": content[:400],
                "cta_button": "LEARN_MORE",
            }

        campaign_id = self.create_campaign(campaign_name, objective)
        adset_id = self.create_adset(
            campaign_id,
            name=f"{campaign_name} — AdSet",
            daily_budget_eur=daily_budget,
        )
        image_hash = self.upload_image(self.image_path)
        creative_id = self.create_adcreative(
            name=f"{campaign_name} — Creative",
            message=creative.get("primary_text", ""),
            link=metadata.get("link", "https://shop.fabiabox.com"),
            headline=creative.get("headline", ""),
            image_hash=image_hash,
            cta_type=creative.get("cta_button", "LEARN_MORE"),
        )
        ad_id = self.create_ad(adset_id, creative_id, name=f"{campaign_name} — Ad")

        return {
            "status": "created",
            "platform": "meta",
            "campaign_id": campaign_id,
            "adset_id": adset_id,
            "creative_id": creative_id,
            "ad_id": ad_id,
            "ad_status": self.status,
        }
