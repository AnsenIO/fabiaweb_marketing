import json

from typing import List

from .content_brief import ContentBrief
from .llm_client import LLMClient


SYSTEM_PROMPT = """You are FABIABox's marketing copywriter.
Brand: "The AI Co-Founder That Ships Your Company."
Product: Fabia is the AI Agent that turns your idea into a live product and business.
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
            "meta": self.generate_meta_variants(brief),
        }

    def generate_meta_variants(self, brief: ContentBrief) -> List[dict]:
        """Return multiple Meta ad creative variants for A/B testing."""
        variants = [
            self._variant_core(brief),
            self._variant_founders(brief),
            self._variant_speed(brief),
            self._variant_no_code(brief),
        ]
        return [
            self._parse_meta(v) if isinstance(v, str) else v
            for v in variants
        ]

    def _parse_meta(self, text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "headline": "Ship your company with AI",
                "primary_text": text[:400],
                "cta_button": "Learn More",
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
  "subject": "Fabia can ship your company",
  "preview": "From idea to launched product without writing code.",
  "body": "<h1>You have the idea. Fabia ships the company.</h1><p>{brief.product} takes your documents and turns them into a live product. {brief.cta}</p><p><a href='{brief.link or 'https://shop.fabiabox.com'}'>Start here →</a></p>"
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
        return json.dumps(
            {
                "headline": "Fabia ships your company",
                "primary_text": f"{brief.product} is the AI Agent that turns your idea into a live product and business. No coding required. {brief.cta}",
                "cta_button": "Learn More",
            }
        )

    def _variant_core(self, brief: ContentBrief) -> dict:
        return {
            "headline": "Idea → live product",
            "primary_text": f"Fabia is the AI Agent that turns your idea into a live product and business. Share your docs, approve the plan, and watch it ship. {brief.cta}",
            "cta_button": "Learn More",
        }

    def _variant_founders(self, brief: ContentBrief) -> dict:
        return {
            "headline": "No tech co-founder? No problem.",
            "primary_text": f"Most founders have the idea but no dev team. {brief.product} builds the product, the business logic, and the go-to-market stack for you. {brief.cta}",
            "cta_button": "Learn More",
        }

    def _variant_speed(self, brief: ContentBrief) -> dict:
        return {
            "headline": "OWN YOUR AI. SHIP YOUR COMPANY.",
            "primary_text": f"You have the idea. {brief.product} turns it into a launched product and business \u2014 without a dev team, without cloud lock-in, and without giving away your data. Approve the plan and ship from the box on your desk.",
            "cta_button": "Learn More",
        }

    def _variant_no_code(self, brief: ContentBrief) -> dict:
        return {
            "headline": "Build a company without coding",
            "primary_text": f"You bring the idea and documents. {brief.product} turns them into a real product, brand, and operating business. You stay in control. {brief.cta}",
            "cta_button": "Learn More",
        }
