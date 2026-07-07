import requests

from .base import Publisher


class EmailPublisher(Publisher):
    name = "email"

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.url = cfg.get("mailtrain_url", "").rstrip("/")
        self.api_key = cfg.get("mailtrain_api_key", "")
        self.list_id = cfg.get("mailtrain_list_id", "")
        self.sender = cfg.get("sender", "andrea@iabai.com")

    def publish(self, content: str, metadata: dict) -> dict:
        if not self.url or not self.api_key:
            return {"status": "skipped", "reason": "missing Mailtrain credentials"}

        payload = {
            "listId": self.list_id,
            "subject": metadata.get("subject", "FABIABox update"),
            "html": content,
            "from": self.sender,
        }
        try:
            resp = requests.post(
                f"{self.url}/api/campaigns",
                headers={"X-Access-Token": self.api_key},
                json=payload,
                timeout=30,
            )
            return {"status": resp.status_code, "body": resp.text[:200]}
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}
