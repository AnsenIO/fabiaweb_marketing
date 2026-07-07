from .base import Publisher


class MetaPublisher(Publisher):
    name = "meta"

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.ad_account_id = cfg.get("ad_account_id", "")
        self.access_token = cfg.get("access_token", "")
        self.pixel_id = cfg.get("pixel_id", "")

    def publish(self, content: str, metadata: dict) -> dict:
        if not self.ad_account_id or not self.access_token:
            return {"status": "skipped", "reason": "missing Meta ad account or access token"}

        # TODO: create campaign/adset/adcreative via Marketing API
        return {
            "status": "published",
            "platform": "meta",
            "ad_account": self.ad_account_id,
            "creative": metadata,
        }
