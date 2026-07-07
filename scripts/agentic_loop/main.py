import argparse

from .config import load_config
from .content_brief import ContentBrief
from .orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(description="FABIABox agentic marketing loop")
    parser.add_argument("--angle", default="founder transformation", help="Content angle")
    parser.add_argument("--audience", default="idea-first founder", help="Target audience")
    parser.add_argument("--product", default="Agentic Build Plan", help="Product to promote")
    parser.add_argument("--cta", default="Join the waitlist →", help="Call to action")
    parser.add_argument("--link", default="https://shop.fabiabox.com", help="Link to include")
    parser.add_argument(
        "--channels", default="email,twitter,meta", help="Comma-separated channels"
    )
    parser.add_argument(
        "--run", action="store_true", help="Actually publish (default is dry-run)"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate Meta API credentials without publishing"
    )
    parser.add_argument(
        "--report", action="store_true", help="Print Meta insights report"
    )
    parser.add_argument(
        "--ab-test", action="store_true", help="Create an A/B test campaign on Meta"
    )
    args = parser.parse_args()

    cfg = load_config()

    if args.report:
        from .reporting.meta_insights import MetaInsights

        insights = MetaInsights(cfg["channels"]["meta"])
        rows = insights.fetch(level="ad", date_preset="last_7d")
        insights.print_report(rows)
        return

    if args.validate:
        print("🔍 Validating Meta API credentials...")
        orchestrator = Orchestrator(cfg, dry_run=True)
        try:
            result = orchestrator.validate_meta()
            print("✅ Meta credentials valid:")
            print(f"  User: {result['user'].get('name')} ({result['user'].get('id')})")
            print(
                f"  Ad account: {result['ad_account'].get('name')} ({result['ad_account'].get('account_id')})"
            )
            print(f"  Status: {result['ad_account'].get('account_status')}")
            print(f"  Existing campaigns: {len(result['existing_campaigns'])}")
        except Exception as exc:
            print(f"❌ Validation failed: {exc}")
        return

    dry_run = not args.run
    if dry_run:
        print("🔶 DRY-RUN mode. No content will be published.")
    else:
        print(
            "🔴 LIVE mode. Campaigns will be created with status: "
            + cfg["channels"]["meta"].get("ad_status", "PAUSED")
        )

    brief = ContentBrief(
        angle=args.angle,
        audience=args.audience,
        product=args.product,
        cta=args.cta,
        link=args.link,
        channels=[c.strip() for c in args.channels.split(",")],
    )

    orchestrator = Orchestrator(cfg, dry_run=dry_run)
    if args.ab_test and "meta" in brief.channels:
        results = orchestrator.run_meta_ab_test(brief)
    else:
        results = orchestrator.run(brief)

    print("\n📊 Results:")
    for channel, result in results.items():
        print(f"  {channel}: {result}")


if __name__ == "__main__":
    main()
