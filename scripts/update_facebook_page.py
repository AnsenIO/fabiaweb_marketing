#!/usr/bin/env python3
"""Update the SquadShelf Facebook page with FABIABox branding."""
import sys

sys.path.insert(0, "scripts")

from agentic_loop.config import load_config
from agentic_loop.publishers.meta import MetaPublisher


def main():
    cfg = load_config()
    publisher = MetaPublisher(cfg["channels"]["meta"])

    updates = {
        "name": "FABIABox",
        "about": "The AI Co-Founder That Ships Your Company.",
        "description": "Fabia is the AI Agent that turns your idea into a live product and business. Built for non-technical founders in Europe. Own your AI, your data, and your stack.",
        "website": "https://fabiabox.com",
        "phone": "+33 4 84 25 00 00",
        "company_overview": "FABIABox helps founders go from idea to operating company using localized AI agents that build, launch, and run the business with you.",
        "mission": "Make every founder capable of shipping a real company without renting their intelligence from a cloud provider.",
        "general_info": "Pre-seed stage. Based in Marseille, France. Serving European entrepreneurs.",
    }

    results = {}
    for field, value in updates.items():
        try:
            result = publisher.update_page({field: value})
            results[field] = result.get("success", True)
            print(f"✅ Updated {field}")
        except Exception as exc:
            results[field] = str(exc)
            print(f"❌ Failed {field}: {exc}")

    print("\nResults:", results)


if __name__ == "__main__":
    main()
