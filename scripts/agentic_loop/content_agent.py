from .content_brief import ContentBrief
from .llm_client import LLMClient


SYSTEM_PROMPT = """You are FABIABox's marketing copywriter.
Brand: "The AI Co-Founder That Ships Your Company."
Voice: direct, pragmatic, founder-to-founder, European, EUR currency.
Rules:
- Lead with outcomes.
- Avoid hype words; use proof.
- Every piece needs a clear CTA.
- Keep tweets under 280 chars each.
"""


class ContentAgent:
    def __init__(self, llm_cfg: dict):
        self.llm = LLMClient(llm_cfg)

    def generate(self, brief: ContentBrief) -> dict:
        return {
            "email": self._email(brief),
            "twitter": self._twitter(brief),
            "discord": self._discord(brief),
            "meta": self._meta(brief),
        }

    def _email(self, brief: ContentBrief) -> str:
        prompt = f"""Write a short marketing email for FABIABox.
Angle: {brief.angle}
Audience: {brief.audience}
Product: {brief.product}
Proof point: {brief.proof_point or 'none'}
CTA: {brief.cta}
Link: {brief.link or 'https://shop.fabiabox.com'}

Return ONLY JSON with keys: subject, preview, body (HTML)."""
        result = self.llm.generate(SYSTEM_PROMPT, prompt)
        if result.startswith("[LLM call failed"):
            return self._email_template(brief)
        return result

    def _email_template(self, brief: ContentBrief) -> str:
        return f"""{{
  "subject": "FABIABox can ship your company",
  "preview": "From idea to launched product without writing code.",
  "body": "<h1>You have the idea. We ship the company.</h1><p>{brief.product} takes your documents and turns them into a live product. {brief.cta}</p><p><a href='{brief.link or 'https://shop.fabiabox.com'}'>Start here →</a></p>"
}}"""

    def _twitter(self, brief: ContentBrief) -> str:
        prompt = f"""Write a 3-5 tweet thread for FABIABox.
Angle: {brief.angle}
Audience: {brief.audience}
Product: {brief.product}
CTA: {brief.cta}
Link: {brief.link or 'https://shop.fabiabox.com'}

Return each tweet on a new line prefixed with the number."""
        result = self.llm.generate(SYSTEM_PROMPT, prompt)
        if result.startswith("[LLM call failed"):
            return self._twitter_template(brief)
        return result

    def _twitter_template(self, brief: ContentBrief) -> str:
        return f"""1/ Most founders get stuck between idea and shipped product.
2/ {brief.product} turns your docs into a live company — no coding required.
3/ You stay in control: approve the plan, own the stack, sign off on legal.
4/ {brief.cta}
5/ {brief.link or 'https://shop.fabiabox.com'}"""

    def _discord(self, brief: ContentBrief) -> str:
        prompt = f"""Write a Discord announcement (max 400 chars) for FABIABox.
Angle: {brief.angle}
Audience: {brief.audience}
Product: {brief.product}
CTA: {brief.cta}
Link: {brief.link or 'https://shop.fabiabox.com'}

Return plain text."""
        result = self.llm.generate(SYSTEM_PROMPT, prompt)
        if result.startswith("[LLM call failed"):
            return self._discord_template(brief)
        return result

    def _discord_template(self, brief: ContentBrief) -> str:
        return f"""🚀 New FABIABox update: {brief.product} is built for founders who want to ship without a tech co-founder. {brief.cta} {brief.link or 'https://shop.fabiabox.com'}
""".strip()

    def _meta(self, brief: ContentBrief) -> str:
        prompt = f"""Write Meta ad creative (headline + primary text + CTA button) for FABIABox.
Angle: {brief.angle}
Audience: {brief.audience}
Product: {brief.product}
CTA: {brief.cta}
Link: {brief.link or 'https://shop.fabiabox.com'}

Return ONLY JSON with keys: headline, primary_text, cta_button."""
        result = self.llm.generate(SYSTEM_PROMPT, prompt)
        if result.startswith("[LLM call failed"):
            return self._meta_template(brief)
        return result

    def _meta_template(self, brief: ContentBrief) -> str:
        return f"""{{
  "headline": "Ship your company with AI",
  "primary_text": "{brief.product} turns your idea and documents into a live product. No coding required. {brief.cta}",
  "cta_button": "Learn More"
}}"""
