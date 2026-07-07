# X/Twitter — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage X/Twitter presence and campaigns for FABIABox.

---

## Twitter API Setup

### Authentication

1. Create a Twitter Developer account
2. Create a new app in the Developer Portal
3. Generate API keys (Bearer Token, API Key, API Secret)
4. Set up OAuth2 for user context (if needed for posting)
5. Get access to Twitter API v2 endpoints

### MCP Server Setup

```bash
# Install Twitter MCP server
npm install @twitter/marketing-mcp-server

# Configure
export TWITTER_BEARER_TOKEN="your_bearer_token"
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Post tweet | `/2/tweets` | POST |
| Get tweet | `/2/tweets/{id}` | GET |
| Media upload | `/2/media` | POST |
| Lists | `/2/lists` | GET/POST |
| Bookmarks | `/2/users/{id}/bookmarks` | GET |
| Mentions | `/2/users/{id}/mentions` | GET |
| Search | `/2/tweets/search/recent` | GET |
| Analytics | `/2/tweets/{id}/analytics` | GET |
| Promoted tweets | `/promoted_tweets` | POST (ads API) |

---

## Agent Instructions for X/Twitter

### Phase 1: Content Strategy

```python
class TwitterContentAgent:
    def plan_content(self):
        """Plan FABIABox Twitter content strategy."""
        
        content_pillars = {
            "technical": {
                "description": "Deep-dives into FABIABox architecture and technology",
                "frequency": "2-3x/week",
                "formats": ["threads", "technical diagrams", "benchmarks"],
                "topics": [
                    "AMD Ryzen AI Max+ architecture",
                    "NVIDIA Thor edge computing",
                    "DGX Spark performance benchmarks",
                    "Sovereign AI infrastructure design",
                    "Agentic AI service architecture"
                ]
            },
            "product": {
                "description": "Product updates, features, and pre-order info",
                "frequency": "1-2x/week",
                "formats": ["product announcements", "comparison threads", "pricing updates"],
                "topics": [
                    "FABIABox Entry — AMD Ryzen AI Max+",
                    "FABIABox Edge — NVIDIA Thor",
                    "FABIABox Pro — DGX Spark",
                    "FABIABox Enterprise — DGX roadmap",
                    "Agentic Build Plan features",
                    "Agentic Operate Plan features"
                ]
            },
            "industry": {
                "description": "AI industry trends and thought leadership",
                "frequency": "2-3x/week",
                "formats": ["opinion threads", "industry analysis", "commentary"],
                "topics": [
                    "Sovereign AI movement",
                    "Edge AI vs cloud AI",
                    "AI infrastructure trends",
                    "AGI development timeline",
                    "AI hardware market analysis"
                ]
            },
            "community": {
                "description": "Engagement with AI community",
                "frequency": "Daily",
                "formats": ["replies", "quotes", "retweets", "polls"],
                "topics": [
                    "AI researcher discussions",
                    "Startup founder threads",
                    "Tech influencer content",
                    "Industry event commentary"
                ]
            }
        }
        
        return content_pillars
```

### Phase 2: Tweet Generation

```python
class TwitterTweetAgent:
    def generate_tweets(self, content_type, topic):
        """Generate tweets for FABIABox."""
        
        tweet_templates = {
            "product_announcement": [
                "🚀 FABIABox {product} is now available for pre-order.\n\n{feature1}\n{feature2}\n{feature3}\n\nPre-buy reservation: €500\nPrice on request\n\n{cta}",
                "The {product} is here.\n\n{feature1}\n{feature2}\n{feature3}\n\nPre-order now. €500 reservation.\n\n{cta}"
            ],
            "technical_thread": [
                "🧵 Why sovereign AI infrastructure matters:\n\n1/ {point1}\n2/ {point2}\n3/ {point3}\n4/ {point4}\n5/ {point5}\n\nFABIABox makes it possible.\n\n{cta}",
                "🧵 The future of AI hardware:\n\n{point1}\n{point2}\n{point3}\n\n{product} delivers this.\n\n{cta}"
            ],
            "industry_insight": [
                "{insight}\n\n{context}\n\n{conclusion}\n\n{cta}",
                "Here's what {industry_leader} got wrong about {topic}:\n\n{correction}\n\n{conclusion}\n\n{cta}"
            ],
            "engagement": [
                "What's your biggest challenge with AI infrastructure?\n\n{options}\n\nWe're building FABIABox to solve this. Pre-order now: {link}",
                "Hot take: {controversial_opinion}\n\nThoughts? 👇\n\n{cta}"
            ]
        }
        
        return self.select_and_customize(tweet_templates, content_type, topic)
```

### Phase 3: Engagement Automation

```python
class TwitterEngagementAgent:
    def engage(self):
        """Automate FABIABox Twitter engagement."""
        
        # Monitor relevant conversations
        conversations = self.monitor_conversations([
            "sovereign AI", "AI hardware", "edge computing",
            "NVIDIA DGX", "AI infrastructure", "AGI",
            "AI startup", "AI co-founder"
        ])
        
        # Auto-generate relevant responses
        for conversation in conversations:
            if self.is_relevant(conversation, "fabiabox"):
                response = self.generate_response(conversation)
                self.post_reply(conversation["author"], response)
                
                # Track engagement
                self.track_engagement(conversation["id"])
        
        # Monitor competitor mentions
        competitors = self.monitor_mentions(["NVIDIA", "AMD", "cloud providers"])
        for mention in competitors:
            if mention.sentiment == "negative":
                # Offer FABIABox as alternative
                response = self.generate_alternative_response(mention)
                self.post_reply(mention["author"], response)
```

### Phase 4: Analytics & Optimization

```python
class TwitterAnalyticsAgent:
    def analyze_performance(self):
        """Analyze FABIABox Twitter performance."""
        
        metrics = {
            "followers": {
                "current": self.get_follower_count(),
                "growth_rate": self.get_follower_growth_rate(),
                "demographics": self.get_follower_demographics()
            },
            "engagement": {
                "impressions": self.get_impressions(),
                "engagements": self.get_engagements(),
                "engagement_rate": self.calculate_engagement_rate(),
                "top_tweets": self.get_top_tweets(limit=10)
            },
            "content_performance": {
                "by_type": self.analyze_by_content_type(),
                "by_topic": self.analyze_by_topic(),
                "by_time": self.analyze_by_posting_time()
            }
        }
        
        # Generate insights
        insights = self.generate_insights(metrics)
        
        # Recommend optimizations
        recommendations = self.generate_recommendations(insights)
        
        return metrics, insights, recommendations
```

---

## Twitter Content Calendar

### Weekly Schedule

| Day | Content Type | Focus |
|-----|-------------|-------|
| Monday | Technical thread | FABIABox architecture deep-dive |
| Tuesday | Industry insight | AI infrastructure trends |
| Wednesday | Product update | FABIABox product news |
| Thursday | Community engagement | Reply to AI community |
| Friday | Technical thread | Benchmark or comparison |
| Saturday | Industry insight | Weekend reading / analysis |
| Sunday | Community engagement | AMA / discussion |

### Hashtag Strategy

| Category | Hashtags | Usage |
|----------|----------|-------|
| Core | #SovereignAI #AIInfrastructure #EdgeComputing | Always |
| Product | #FABIABox #AGI #AIHardware | Product posts |
| Industry | #AI #MachineLearning #DeepLearning #Tech | Industry posts |
| Community | #Startup #Founder #CTO #Engineering | Community posts |
| Trending | Monitor and add trending tags | As relevant |

---

## Promoted Tweets Strategy

### Targeting for FABIABox

| Audience | Criteria | Budget |
|----------|----------|--------|
| AI Researchers | Job title: Researcher, PhD; Interests: AI, ML | €50/day |
| Tech Founders | Job title: Founder, CEO; Company size: 1-50 | €100/day |
| Enterprise IT | Job title: CTO, CIO; Company size: 500+ | €150/day |
| AI Engineers | Job title: ML Engineer, AI Engineer; Interests: AI | €75/day |
| Startup Community | Interests: Startups, Entrepreneurship; Company size: 1-10 | €50/day |

### Ad Copy Templates

```python
promoted_tweets = [
    {
        "text": "Build your own AI infrastructure. No vendor lock-in. Sovereign AI made possible.\n\nFABIABox: From €49.99/mo to enterprise DGX solutions.\n\nPre-order now: {link}",
        "media": "fabiabox-hero.jpg",
        "cta": "Learn More"
    },
    {
        "text": "The AI Co-Founder That Ships Your Company.\n\nAgentic Build Plan: From idea to launched product.\n€49.99/mo or €499/year.\n\nStart building: {link}",
        "media": "agentic-build.jpg",
        "cta": "Sign Up"
    },
    {
        "text": "NVIDIA DGX roadmap (20 PFlop) in a FABIABox Enterprise solution.\n\nPre-buy reservation: €500\nPrice on request\n\nContact us: {link}",
        "media": "fabiabox-enterprise.jpg",
        "cta": "Contact Us"
    }
]
```

---

## Next Steps

1. [ ] Set up Twitter Developer account and API access
2. [ ] Create FABIABox Twitter account (if not exists)
3. [ ] Configure API credentials
4. [ ] Set up content calendar and auto-posting
5. [ ] Implement engagement automation
6. [ ] Set up analytics tracking
7. [ ] Launch promoted tweet campaigns
8. [ ] Begin A/B testing and optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
