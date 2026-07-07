from .content_agent import ContentAgent
from .publishers.discord import DiscordPublisher
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
            "discord": DiscordPublisher(cfg["channels"]["discord"]),
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
