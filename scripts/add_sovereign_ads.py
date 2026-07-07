#!/usr/bin/env python3
"""Add two 'sovereign AI' ad variants to an existing Meta A/B test campaign."""
import sys
import time

sys.path.insert(0, "scripts")

from agentic_loop.config import load_config
from agentic_loop.publishers.meta import MetaPublisher


def main():
    cfg = load_config()["channels"]["meta"]
    publisher = MetaPublisher(cfg)

    # Find the A/B test campaign
    campaign_name = cfg.get("campaigns", {}).get("retargeting_website", {}).get(
        "name", "FABIABox — A/B Test"
    )
    campaign_id = publisher._find_campaign_by_name(campaign_name)
    if not campaign_id:
        raise RuntimeError(f"Campaign not found: {campaign_name}")

    # List adsets
    adsets = publisher._request(
        "GET",
        f"{campaign_id}/adsets",
        params={"fields": "id,name"},
    ).get("data", [])

    if not adsets:
        raise RuntimeError("No adsets found in campaign")

    variants = [
        {
            "headline": "SAAS IS DEAD. SOVEREIGN AI IS BORN.",
            "primary_text": "Take back control of your models, your data, and your future. Fabia runs on your desk, not a cloud provider.",
            "cta_button": "Learn More",
            "image_path": "assets/images/fabia_ad_v5.png",
        },
        {
            "headline": "WHY RENT AI WHEN YOU CAN OWN THE FOUNDRY?",
            "primary_text": "The cloud is someone else's computer. Build your intelligence locally with Fabia.",
            "cta_button": "Learn More",
            "image_path": "assets/images/fabia_ad_v6.png",
        },
    ]

    link = cfg.get("link", "https://shop.fabiabox.com")

    for adset in adsets:
        adset_id = adset["id"]
        print(f"Adding variants to adset {adset_id} ({adset['name']})")
        for idx, variant in enumerate(variants, start=5):
            image_hash = publisher.upload_image(variant["image_path"])
            time.sleep(1)
            creative_id = publisher.create_adcreative(
                name=f"{campaign_name} — {adset['name']} — V{idx}",
                message=variant["primary_text"],
                link=link,
                headline=variant["headline"],
                image_hash=image_hash,
                cta_type=variant["cta_button"],
            )
            time.sleep(1)
            ad_id = publisher.create_ad(
                adset_id,
                creative_id,
                name=f"{campaign_name} — {adset['name']} — Ad V{idx}",
            )
            print(f"  Created V{idx}: ad_id={ad_id}, creative_id={creative_id}")
            time.sleep(1)


if __name__ == "__main__":
    main()
