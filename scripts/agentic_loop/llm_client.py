from openai import OpenAI


class LLMClient:
    def __init__(self, cfg):
        self.client = OpenAI(
            base_url=cfg.get("base_url", "http://127.0.0.1:11435/v1"),
            api_key=cfg.get("api_key") or "not-needed",
        )
        self.model = cfg.get("model", "default")
        self.temperature = cfg.get("temperature", 0.7)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as exc:
            return f"[LLM call failed: {exc}]"
