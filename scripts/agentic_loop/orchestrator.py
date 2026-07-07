import time

from .content_agent import ContentAgent
from .publishers.email import EmailPublisher
from .publishers.meta import MetaPublisher
from .publishers.twitter import TwitterPublisher


class Orchestrator:
    def __init__(self, cfg: dict, dry_run: bool = True):
        self.cfg = cfg
        self.dry_run = dry_run
        self.content_agent = ContentAgent(cfg["llm"])
        self.publishers = {
            "email": EmailPublisher(cfg["channels"]["email"]),
            "twitter": TwitterPublisher(cfg["channels"]["twitter"]),
            "meta": MetaPublisher(cfg["channels"]["meta"]),
        }

    def run(self, brief):
        print(f"\n🚀 Generating content for: {brief.angle}")
        generated = self.content_agent.generate(brief)

        results = {}
        for channel in brief.channels:
            if channel not in generated:
                continue
            content = generated[channel]
            print(f"\n📤 {channel.upper()}:\n{content}\n")

            if self.dry_run:
                results[channel] = {"status": "dry_run", "content_length": len(str(content))}
                continue

            publisher = self.publishers[channel]
            metadata = {"subject": f"FABIABox: {brief.angle}"} if channel == "email" else {}
            if brief.link:
                metadata["link"] = brief.link
            results[channel] = publisher.publish(str(content), metadata)

        return results

    def validate_meta(self) -> dict:
        publisher = self.publishers["meta"]
        return publisher.validate()

    def run_meta_ab_test(self, brief):
        print(f"\n🚀 Running Meta A/B test for: {brief.angle}")

        if self.dry_run:
            print("🔶 DRY-RUN mode. No ads will be published.")
            variants = self.content_agent.generate_meta_variants(brief)
            for i, v in enumerate(variants, 1):
                print(f"  Variant {i}: {v.get('headline')}")
            return {"meta": {"status": "dry_run", "variants": len(variants)}}

        publisher = self.publishers["meta"]
        cfg = self.cfg["channels"]["meta"]
        campaign_cfg = cfg.get("campaigns", {}).get("retargeting_website", {})
        campaign_name = campaign_cfg.get("name", "FABIABox — A/B Test")
        objective = campaign_cfg.get("objective", "OUTCOME_TRAFFIC")

        variants = self.content_agent.generate_meta_variants(brief)
        image_paths = cfg.get("image_paths", [cfg.get("image_path")])
        ab_cfg = cfg.get("ab_test", {})
        adsets_cfg = ab_cfg.get("adsets", [
            {"name": "EU Founders", "countries": ["FR", "DE", "GB", "ES", "IT", "NL"], "daily_budget_eur": 10},
            {"name": "FR Founders", "countries": ["FR"], "daily_budget_eur": 10},
        ])

        campaign_id = publisher.create_campaign(campaign_name, objective)
        time.sleep(1)

        created = {"campaign_id": campaign_id, "adsets": []}
        for adset_cfg in adsets_cfg:
            targeting = {
                "geo_locations": {"countries": adset_cfg["countries"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0},
            }
            adset_id = publisher.create_adset(
                campaign_id,
                name=f"{campaign_name} — {adset_cfg['name']}",
                daily_budget_eur=adset_cfg["daily_budget_eur"],
                targeting=targeting,
            )
            time.sleep(1)

            ads = []
            for idx, variant in enumerate(variants):
                image_path = image_paths[idx % len(image_paths)]
                image_hash = publisher.upload_image(image_path)
                time.sleep(1)

                creative_id = publisher.create_adcreative(
                    name=f"{campaign_name} — {adset_cfg['name']} — V{idx + 1}",
                    message=variant.get("primary_text", ""),
                    link=brief.link or "https://shop.fabiabox.com",
                    headline=variant.get("headline", ""),
                    image_hash=image_hash,
                    cta_type=variant.get("cta_button", "LEARN_MORE"),
                )
                time.sleep(1)

                ad_id = publisher.create_ad(
                    adset_id,
                    creative_id,
                    name=f"{campaign_name} — {adset_cfg['name']} — Ad V{idx + 1}",
                )
                ads.append({"variant": idx + 1, "ad_id": ad_id, "creative_id": creative_id})
                time.sleep(1)

            created["adsets"].append({"adset_id": adset_id, "ads": ads})

        return {"meta": {"status": "created", "ab_test": created}}
