import requests

from .base import Publisher


class DiscordPublisher(Publisher):
    name = "discord"

    def __init__(self, cfg: dict):
        self.webhook_url = cfg.get("webhook_url", "")

    def publish(self, content: str, metadata: dict) -> dict:
        if not self.webhook_url:
            return {"status": "skipped", "reason": "missing DISCORD_WEBHOOK_URL"}

        try:
            resp = requests.post(
                self.webhook_url,
                json={"content": content},
                timeout=30,
            )
            return {"status": resp.status_code, "body": resp.text[:200]}
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}
