# Meta (Facebook & Instagram) Ads — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage Meta (Facebook & Instagram) Ads campaigns for FABIABox.

---

## Meta Marketing API Setup

### Authentication

1. Create a Meta Developer account
2. Create a new app in the Developer Portal
3. Generate App ID and App Secret
4. Get Marketing API access
5. Create ad account and get ad account ID
6. Set up OAuth2 for user context

### MCP Server Setup

```bash
# Install Meta Marketing MCP server
npm install @meta/marketing-mcp-server

# Configure
export META_APP_ID="your_app_id"
export META_APP_SECRET="your_app_secret"
export META_ACCESS_TOKEN="your_access_token"
export META_AD_ACCOUNT_ID="your_ad_account_id"
export META_BUSINESS_MANAGER_ID="your_business_manager_id"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Ad accounts | `/v19.0/{ad_account_id}` | GET |
| Campaigns | `/{ad_account_id}/campaigns` | GET/POST |
| Ad groups | `/{ad_account_id}/adsets` | GET/POST |
| Ads | `/{ad_account_id}/ads` | GET/POST |
| Creatives | `/{ad_account_id}/adcreatives` | GET/POST |
| Images | `/{ad_account_id}/images` | POST |
| Videos | `/{ad_account_id}/videos` | POST |
| Carousels | `/{ad_account_id}/adcreatives` | POST |
| Audiences | `/{ad_account_id}/customaudiences` | GET/POST |
| Insights | `/{ad_account_id}/insights` | GET |

---

## Agent Instructions for Meta Ads

### Phase 1: Audience Building

```python
class MetaAudienceAgent:
    def build_audiences(self):
        """Build targeted audiences for FABIABox."""
        
        audiences = {
            "custom_audiences": {
                "pre_order_list": {
                    "name": "FABIABox Pre-Order List",
                    "type": "CUSTOM",
                    "source": "email_list",
                    "data": "pre_order_emails.csv"
                },
                "website_visitors": {
                    "name": "FABIABox Website Visitors",
                    "type": "CUSTOM",
                    "source": "pixel",
                    "retention_days": 180
                },
                "content_engagers": {
                    "name": "FABIABox Content Engagers",
                    "type": "CUSTOM",
                    "source": "engagement",
                    "retention_days": 90
                }
            },
            "lookalike_audiences": {
                "pre_order_lookalike": {
                    "name": "FABIABox Pre-Order Lookalike",
                    "type": "LOOKALIKE",
                    "source": "pre_order_list",
                    "regions": ["EU", "US", "APAC"]
                },
                "website_lookalike": {
                    "name": "FABIABox Website Lookalike",
                    "type": "LOOKALIKE",
                    "source": "website_visitors",
                    "regions": ["EU", "US", "APAC"]
                }
            },
            "interest_audiences": {
                "ai_enthusiasts": ["Artificial Intelligence", "Machine Learning", "Deep Learning"],
                "tech_founders": ["Startup", "Entrepreneurship", "Technology"],
                "enterprise_it": ["Enterprise Software", "Cloud Computing", "Data Center"],
                "hardware_enthusiasts": ["NVIDIA", "AMD", "Computer Hardware"]
            }
        }
        
        return audiences
```

### Phase 2: Campaign Creation

```python
class MetaCampaignAgent:
    def create_campaigns(self, audiences):
        """Create Meta campaigns for FABIABox."""
        
        campaigns = {
            "hardware_sales": {
                "name": "FABIABox Hardware — Sales",
                "objective": "CONVERSIONS",
                "special_ad_categories": "NONE",
                "budget": {
                    "daily": 500,  # €500/day
                    "currency": "EUR"
                },
                "optimization_goal": "LINK_CLICKS",
                "bidding_strategy": "LOWEST_COST_WITH_CAP",
                "target_cpa": 500  # €500 target CPA
            },
            "lead_generation": {
                "name": "FABIABox — Lead Generation",
                "objective": "LEAD_GENERATION",
                "special_ad_categories": "NONE",
                "budget": {
                    "daily": 300,  # €300/day
                    "currency": "EUR"
                },
                "lead_quality": "HIGH_INTENT"
            },
            "brand_awareness": {
                "name": "FABIABox — Brand Awareness",
                "objective": "BRAND_AWARENESS",
                "special_ad_categories": "NONE",
                "budget": {
                    "daily": 200,  # €200/day
                    "currency": "EUR"
                }
            },
            "retargeting": {
                "name": "FABIABox — Retargeting",
                "objective": "CONVERSIONS",
                "special_ad_categories": "NONE",
                "budget": {
                    "daily": 150,  # €150/day
                    "currency": "EUR"
                },
                "audiences": [
                    "website_visitors",
                    "content_engagers",
                    "pre_order_list"
                ]
            }
        }
        
        return campaigns
```

### Phase 3: Creative Generation

```python
class MetaCreativeAgent:
    def generate_ads(self):
        """Generate Meta ad creatives for FABIABox."""
        
        ads = {
            "hardware_carousel": {
                "type": "CAROUSEL",
                "name": "FABIABox Product Tiers",
                "cards": [
                    {
                        "title": "FABIABox Entry",
                        "subtitle": "AMD Ryzen AI Max+",
                        "description": "Startup-friendly AI hardware",
                        "image": "fabiabox-entry.jpg",
                        "cta": "Learn More",
                        "link": "https://shop.fabiabox.com/entry"
                    },
                    {
                        "title": "FABIABox Edge",
                        "subtitle": "NVIDIA Thor",
                        "description": "Edge AI deployment",
                        "image": "fabiabox-edge.jpg",
                        "cta": "Learn More",
                        "link": "https://shop.fabiabox.com/edge"
                    },
                    {
                        "title": "FABIABox Pro",
                        "subtitle": "DGX Spark (1 PFlop)",
                        "description": "AI research hardware",
                        "image": "fabiabox-pro.jpg",
                        "cta": "Learn More",
                        "link": "https://shop.fabiabox.com/pro"
                    },
                    {
                        "title": "FABIABox Enterprise",
                        "subtitle": "DGX Roadmap (20 PFlop)",
                        "description": "Enterprise AI infrastructure",
                        "image": "fabiabox-enterprise.jpg",
                        "cta": "Contact Us",
                        "link": "https://shop.fabiabox.com/enterprise"
                    }
                ]
            },
            "video_ads": {
                "type": "VIDEO",
                "name": "FABIABox Vision",
                "video": "fabiabox-vision.mp4",
                "primary_text": "The AI Co-Founder That Ships Your Company.",
                "headline": "Pre-buy FABIABox hardware or subscribe to agentic services.",
                "description": "From €49.99/mo. Pre-buy reservation: €500.",
                "cta": "Learn More"
            },
            "lead_ads": {
                "type": "LEAD_AD",
                "name": "FABIABox Pre-order Interest",
                "primary_text": "Get priority access to cutting-edge AI hardware.",
                "headline": "Pre-buy FABIABox — €500 Reservation",
                "description": "Join the waiting list or pre-order now.",
                "form": {
                    "fields": ["full_name", "email", "company", "country", "product_interest"],
                    "privacy_policy": "https://fabiabox.com/privacy"
                }
            },
            "image_ads": {
                "type": "IMAGE",
                "name": "FABIABox Sovereign AI",
                "image": "fabiabox-sovereign.jpg",
                "primary_text": "No vendor lock-in. Sovereign AI infrastructure made possible.",
                "headline": "FABIABox — Build Your Own AI Future",
                "description": "From AMD Ryzen AI Max+ to NVIDIA DGX. Pre-order now.",
                "cta": "Learn More"
            }
        }
        
        return ads
```

### Phase 4: Campaign Optimization

```python
class MetaOptimizationAgent:
    def optimize_campaigns(self):
        """Auto-optimize FABIABox Meta campaigns."""
        
        campaigns = self.get_campaign_performance()
        
        for campaign in campaigns:
            # Scale winning campaigns
            if campaign["roas"] > 3.0:
                self.increase_budget(campaign["id"], 20)
                
            # Reduce spend on underperformers
            elif campaign["cpa"] > 600:
                self.decrease_budget(campaign["id"], 25)
                
            # A/B test creatives
            for creative in campaign["creatives"]:
                if creative["ctr"] > 0.02:
                    # Scale winning creative
                    self.increase_budget(campaign["id"], 15)
                elif creative["ctr"] < 0.005:
                    # Pause underperforming creative
                    self.pause_ad(campaign["id"], creative["id"])
            
            # Refresh audiences
            if campaign["days_active"] > 60:
                self.refresh_audiences(campaign["id"])
```

---

## Facebook & Instagram Strategy

### Facebook Strategy

| Aspect | Details |
|--------|---------|
| Primary use | Lead generation, brand awareness |
| Target audience | B2B decision makers, tech founders |
| Content type | Long-form posts, carousel ads, video ads |
| Posting frequency | 3-5x/week (organic), daily (paid) |
| Groups | Join AI/tech groups, share FABIABox insights |

### Instagram Strategy

| Aspect | Details |
|--------|---------|
| Primary use | Brand building, product showcase |
| Target audience | AI enthusiasts, tech founders, developers |
| Content type | Reels, Stories, carousels, product photos |
| Posting frequency | 5-7x/week (organic), daily (paid) |
| Hashtags | #SovereignAI #AIInfrastructure #EdgeComputing #AGI #AIHardware #FABIABox |

### Content Mix

| Content Type | Percentage | Examples |
|-------------|-----------|----------|
| Product showcase | 30% | Hardware photos, product demos |
| Technical content | 25% | Architecture diagrams, benchmarks |
| Behind-the-scenes | 20% | Development updates, team culture |
| Industry insights | 15% | AI trends, thought leadership |
| Community engagement | 10% | Polls, Q&A, user-generated content |

---

## Next Steps

1. [ ] Set up Meta Developer account and API access
2. [ ] Create Meta Business Manager for FABIABox
3. [ ] Configure OAuth2 credentials
4. [ ] Set up Facebook Pixel on fabiabox.com
5. [ ] Build initial audiences
6. [ ] Create campaigns for each product tier
7. [ ] Generate ad creatives (images, videos, carousels)
8. [ ] Launch campaigns and begin A/B testing
9. [ ] Implement automated optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
