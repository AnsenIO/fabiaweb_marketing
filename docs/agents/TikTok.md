# TikTok — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage TikTok presence and campaigns for FABIABox.

---

## TikTok Marketing API Setup

### Authentication

1. Create a TikTok Developer account
2. Create a new app in the Developer Portal
3. Generate API keys (App ID, App Secret)
4. Get Marketing API access
5. Set up OAuth2 for user context

### MCP Server Setup

```bash
# Install TikTok Marketing MCP server
npm install @tiktok/marketing-mcp-server

# Configure
export TIKTOK_APP_ID="your_app_id"
export TIKTOK_APP_SECRET="your_app_secret"
export TIKTOK_ACCESS_TOKEN="your_access_token"
export TIKTOK_BUSINESS_MANAGER_ID="your_business_manager_id"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Campaigns | `/promote/open_api/campaign` | GET/POST |
| Ad groups | `/promote/open_api/adgroup` | GET/POST |
| Ads | `/promote/open_api/creative` | GET/POST |
| Videos | `/promote/open_api/video` | GET/POST |
| Audiences | `/promote/open_api/audience` | GET/POST |
| Reports | `/promote/open_api/report` | GET |

---

## Agent Instructions for TikTok

### Phase 1: Content Strategy

```python
class TikTokContentAgent:
    def plan_content(self):
        """Plan FABIABox TikTok content strategy."""
        
        content_pillars = {
            "behind_the_scenes": {
                "description": "Show the FABIABox development process",
                "frequency": "3-4x/week",
                "formats": ["setup tours", "team introductions", "development updates"],
                "hook_examples": [
                    "Day in the life of an AI hardware engineer",
                    "How we build FABIABox workstations",
                    "The team behind sovereign AI"
                ]
            },
            "quick_explainers": {
                "description": "Short explanations of AI hardware concepts",
                "frequency": "3-4x/week",
                "formats": ["60-second explainers", "myth-busting", "comparison videos"],
                "hook_examples": [
                    "What is sovereign AI? (in 60 seconds)",
                    "NVIDIA DGX vs AMD Ryzen AI — which is better?",
                    "Why edge computing matters for AI"
                ]
            },
            "product_highlights": {
                "description": "Showcase FABIABox products",
                "frequency": "2-3x/week",
                "formats": ["product tours", "benchmarks", "setup demos"],
                "hook_examples": [
                    "Unboxing FABIABox Pro",
                    "1 PFlop AI power in your desk",
                    "Setting up FABIABox in 5 minutes"
                ]
            },
            "trending_content": {
                "description": "Leverage trending audio and formats",
                "frequency": "Daily",
                "formats": ["trend participations", "challenges", "duets"],
                "hook_examples": [
                    "POV: You just got your FABIABox",
                    "When your AI workstation arrives",
                    "AI hardware that fits on your desk"
                ]
            }
        }
        
        return content_pillars
```

### Phase 2: Content Generation

```python
class TikTokCreativeAgent:
    def generate_content(self, content_type):
        """Generate TikTok content for FABIABox."""
        
        content = {
            "behind_the_scenes": [
                {
                    "hook": "This is where the magic happens",
                    "visual": "FABIABox lab tour",
                    "audio": "trending tech audio",
                    "text_overlay": ["AMD Ryzen AI Max+", "NVIDIA Thor", "DGX Spark"],
                    "cta": "Pre-order now — link in bio"
                },
                {
                    "hook": "Building sovereign AI infrastructure",
                    "visual": "Assembly process",
                    "audio": "original audio",
                    "text_overlay": ["Hand-built", "Quality tested", "Ready to ship"],
                    "cta": "Join the waitlist"
                }
            ],
            "quick_explainers": [
                {
                    "hook": "What is sovereign AI?",
                    "visual": "Animation + FABIABox hardware",
                    "audio": "trending explainer audio",
                    "text_overlay": [
                        "No vendor lock-in",
                        "Your data, your control",
                        "FABIABox makes it possible"
                    ],
                    "cta": "Learn more — link in bio"
                },
                {
                    "hook": "NVIDIA DGX vs FABIABox",
                    "visual": "Side-by-side comparison",
                    "audio": "trending comparison audio",
                    "text_overlay": [
                        "DGX: Cloud dependency",
                        "FABIABox: Sovereign",
                        "Which do you prefer?"
                    ],
                    "cta": "Comment below 👇"
                }
            ],
            "product_highlights": [
                {
                    "hook": "1 PFlop AI power on your desk",
                    "visual": "FABIABox Pro unboxing",
                    "audio": "trending tech audio",
                    "text_overlay": ["DGX Spark", "1 PFlop", "Pre-order now"],
                    "cta": "€500 reservation — link in bio"
                },
                {
                    "hook": "Setting up FABIABox in 5 minutes",
                    "visual": "Time-lapse setup",
                    "audio": "fast-paced trending audio",
                    "text_overlay": ["Plug in", "Power on", "Ready"],
                    "cta": "So easy — pre-order now"
                }
            ]
        }
        
        return content
```

### Phase 3: Campaign Management

```python
class TikTokCampaignAgent:
    def create_campaigns(self):
        """Create TikTok campaigns for FABIABox."""
        
        campaigns = {
            "brand_awareness": {
                "name": "FABIABox Brand Awareness",
                "objective": "BRAND_AWARENESS",
                "budget": {
                    "daily": 200,  # €200/day
                    "currency": "EUR"
                },
                "targeting": {
                    "interests": ["AI", "Machine Learning", "Technology", "Startups"],
                    "age_range": "25-45",
                    "regions": ["EU", "US", "APAC"]
                }
            },
            "lead_generation": {
                "name": "FABIABox Lead Generation",
                "objective": "LEAD_GENERATION",
                "budget": {
                    "daily": 150,  # €150/day
                    "currency": "EUR"
                },
                "targeting": {
                    "interests": ["AI Hardware", "Edge Computing", "Sovereign AI"],
                    "age_range": "25-55",
                    "job_titles": ["CTO", "CIO", "VP of Engineering", "Founder"]
                }
            },
            "website_traffic": {
                "name": "FABIABox Website Traffic",
                "objective": "WEBSITE_TRAFFIC",
                "budget": {
                    "daily": 100,  # €100/day
                    "currency": "EUR"
                },
                "targeting": {
                    "interests": ["Technology", "AI", "Startups"],
                    "age_range": "25-45"
                }
            }
        }
        
        return campaigns
```

### Phase 4: Analytics & Optimization

```python
class TikTokAnalyticsAgent:
    def analyze_performance(self):
        """Analyze FABIABox TikTok performance."""
        
        metrics = {
            "content": {
                "views": self.get_total_views(),
                "likes": self.get_total_likes(),
                "shares": self.get_total_shares(),
                "comments": self.get_total_comments(),
                "follower_growth": self.get_follower_growth_rate()
            },
            "top_videos": self.get_top_videos(limit=10),
            "audience": {
                "demographics": self.get_audience_demographics(),
                "interests": self.get_audience_interests(),
                "peak_activity": self.get_peak_activity_times()
            },
            "campaigns": {
                "cpm": self.get_campaign_cpm(),
                "ctr": self.get_campaign_ctr(),
                "cpv": self.get_campaign_cpv(),
                "roas": self.get_campaign_roas()
            }
        }
        
        # Generate insights
        insights = self.generate_insights(metrics)
        
        # Recommend optimizations
        recommendations = self.generate_recommendations(insights)
        
        return metrics, insights, recommendations
```

---

## TikTok Best Practices

### Content Guidelines

- **Hook in first 2 seconds** — grab attention immediately
- **Use trending audio** — increases discoverability
- **Keep it authentic** — TikTok users value genuine content
- **Vertical format only** — 9:16 aspect ratio
- **Add text overlays** — many watch without sound
- **Include CTA** — drive to link in bio or website

### Posting Schedule

| Time | Audience | Content Type |
|------|----------|-------------|
| 9-11 AM | EU audience | Behind-the-scenes |
| 12-2 PM | Global | Quick explainers |
| 6-8 PM | US audience | Product highlights |
| 8-10 PM | Global | Trending content |

### Hashtag Strategy

| Category | Hashtags | Usage |
|----------|----------|-------|
| Core | #SovereignAI #AIInfrastructure #FABIABox | Always |
| Tech | #AI #MachineLearning #EdgeComputing #AGI | Tech content |
| Trending | Monitor and add trending tags | As relevant |
| Niche | #AIHardware #DataCenter #TechStartup | Product content |

---

## Next Steps

1. [ ] Set up TikTok Business account for FABIABox
2. [ ] Create TikTok Developer account and API access
3. [ ] Configure API credentials
4. [ ] Plan initial content calendar
5. [ ] Create first batch of TikTok videos
6. [ ] Set up TikTok Ads Manager
7. [ ] Launch initial campaigns
8. [ ] Begin analytics tracking and optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
