import argparse

from .config import load_config
from .content_brief import ContentBrief
from .orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(description="FABIABox agentic marketing loop")
    parser.add_argument(
        "--angle", default="founder transformation", help="Content angle"
    )
    parser.add_argument("--audience", default="idea-first founder", help="Target audience")
    parser.add_argument("--product", default="Agentic Build Plan", help="Product to promote")
    parser.add_argument("--cta", default="Join the waitlist →", help="Call to action")
    parser.add_argument("--link", default="https://shop.fabiabox.com", help="Link to include")
    parser.add_argument(
        "--channels", default="email,twitter,discord,meta", help="Comma-separated channels"
    )
    parser.add_argument(
        "--run", action="store_true", help="Actually publish (default is dry-run)"
    )
    args = parser.parse_args()

    cfg = load_config()
    dry_run = not args.run
    if dry_run:
        print("🔶 DRY-RUN mode. No content will be published.")

    brief = ContentBrief(
        angle=args.angle,
        audience=args.audience,
        product=args.product,
        cta=args.cta,
        link=args.link,
        channels=[c.strip() for c in args.channels.split(",")],
    )

    orchestrator = Orchestrator(cfg, dry_run=dry_run)
    results = orchestrator.run(brief)

    print("\n📊 Results:")
    for channel, result in results.items():
        print(f"  {channel}: {result}")


if __name__ == "__main__":
    main()
