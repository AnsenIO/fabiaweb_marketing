# LinkedIn Ads — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage LinkedIn Ads campaigns for FABIABox B2B marketing.

---

## LinkedIn Marketing Developer Platform Setup

### Authentication

1. Create a LinkedIn Developer account
2. Create a new app in the Marketing Developer Platform
3. Generate API keys (Client ID, Client Secret)
4. Set up OAuth2 redirect URI
5. Request API access for ad creation and management

### MCP Server Setup

```bash
# Install LinkedIn MCP server
npm install @linkedin/marketing-mcp-server

# Configure
export LINKEDIN_CLIENT_ID="your_client_id"
export LINKEDIN_CLIENT_SECRET="your_client_secret"
export LINKEDIN_REDIRECT_URI="https://fabiabox.com/linkedin/callback"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Campaigns | `/campaigns/v2/campaigns` | GET/POST |
| Ad creatives | `/adCreatives` | GET/POST |
| Sponsored content | `/ugcPosts` | GET/POST |
| Text ads | `/adDeliveryMethods/TEXT_AD` | POST |
| Message ads | `/adDeliveryMethods/DIRECT_MESSAGE` | POST |
| Lead gen forms | `/leadGenForms` | GET/POST |
| Matched audiences | `/matchedAudiences` | GET/POST |
| Reports | `/campaigns/v2/campaigns/{id}/reports` | GET |

---

## Agent Instructions for LinkedIn Ads

### Phase 1: Audience Targeting

```python
class LinkedInAudienceAgent:
    def build_audiences(self):
        """Build targeted audiences for FABIABox."""
        
        audiences = {
            "job_titles": [
                "CTO", "CIO", "VP of Engineering", "Chief Technology Officer",
                "AI Lead", "Head of AI", "Director of AI", "ML Engineer",
                "Data Science Director", "VP of Data Science",
                "Founder", "CEO", "Co-founder", "Technical Founder",
                "Head of Engineering", "Engineering Manager",
                "Product Manager", "VP of Product"
            ],
            "industries": [
                "Artificial Intelligence", "Computer Software",
                "Information Technology", "Semiconductors",
                "Cloud Computing", "Data Infrastructure",
                "Enterprise Software", "Research Services"
            ],
            "company_sizes": ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000"],
            "seniority_levels": ["Director", "VP", "C-Suite", "Owner", "Partner"],
            "matched_audiences": {
                "website_visitors": "fabiabox.com visitors",
                "pre_order_list": "pre-order email list",
                "content_engagers": "research page readers",
                "lookalike": "lookalike of pre-order list"
            }
        }
        
        return audiences
```

### Phase 2: Campaign Creation

```python
class LinkedInCampaignAgent:
    def create_campaigns(self, audiences):
        """Create LinkedIn campaigns for FABIABox."""
        
        campaigns = {
            "enterprise_hardware": {
                "name": "FABIABox Enterprise — LinkedIn",
                "type": "CAMPAIGN",
                "status": "ACTIVE",
                "budget": {
                    "amount": 2000,
                    "currency_code": "EUR",
                    "frequency_cap": "DAILY"
                },
                "targeting": {
                    "geo": ["Europe", "North America", "Asia Pacific"],
                    "job_titles": audiences["job_titles"],
                    "industries": audiences["industries"],
                    "company_sizes": audiences["company_sizes"],
                    "seniority": audiences["seniority_levels"]
                },
                "ad_delivery": "TEXT_AD",
                "objective": "LEAD_GENERATION"
            },
            "thought_leadership": {
                "name": "FABIABox Thought Leadership — LinkedIn",
                "type": "CAMPAIGN",
                "status": "ACTIVE",
                "budget": {
                    "amount": 1000,
                    "currency_code": "EUR",
                    "frequency_cap": "DAILY"
                },
                "targeting": {
                    "geo": ["Global"],
                    "job_titles": ["CTO", "CIO", "VP of Engineering", "AI Lead"],
                    "seniority": ["Director", "VP", "C-Suite"]
                },
                "ad_delivery": "SPONSORED_CONTENT",
                "objective": "WEBSITE_VISITS"
            },
            "lead_gen_form": {
                "name": "FABIABox Pre-order — LinkedIn Lead Gen",
                "type": "CAMPAIGN",
                "status": "ACTIVE",
                "budget": {
                    "amount": 1500,
                    "currency_code": "EUR",
                    "frequency_cap": "DAILY"
                },
                "targeting": {
                    "geo": ["Europe", "North America"],
                    "job_titles": ["CTO", "CIO", "VP of Engineering", "Founder"],
                    "industries": ["Artificial Intelligence", "Computer Software", "Enterprise Software"]
                },
                "ad_delivery": "LEAD_GEN_FORM",
                "objective": "LEAD_GENERATION"
            }
        }
        
        return campaigns
```

### Phase 3: Ad Creative Generation

```python
class LinkedInCreativeAgent:
    def generate_ads(self):
        """Generate LinkedIn ad creatives for FABIABox."""
        
        ads = {
            "enterprise_hardware": [
                {
                    "type": "TEXT_AD",
                    "text": {
                        "headline": "FABIABox Enterprise — NVIDIA DGX Roadmap Access",
                        "body": "20 PFlop of AI power. Sovereign infrastructure. Pre-buy reservation at €500. Contact us for pricing and delivery timeline.",
                        "cta": "Contact Us"
                    },
                    "targeting": "B2B decision makers in AI/tech"
                },
                {
                    "type": "TEXT_AD",
                    "text": {
                        "headline": "Sovereign AI Infrastructure — FABIABox",
                        "body": "No vendor lock-in. Build your own AI infrastructure. From AMD Ryzen AI Max+ to NVIDIA DGX. Pre-order now.",
                        "cta": "Learn More"
                    }
                }
            ],
            "thought_leadership": [
                {
                    "type": "SPONSORED_CONTENT",
                    "post": {
                        "text": "The future of AI infrastructure is sovereign. FABIABox gives you the hardware and agentic services to build your own AI company — no cloud dependency, no vendor lock-in.\n\nFrom €49.99/mo for the Agentic Build Plan to enterprise DGX solutions.\n\n#SovereignAI #AIInfrastructure #EdgeComputing",
                        "media": {
                            "type": "IMAGE",
                            "url": "https://fabiabox.com/images/fabiabox-enterprise.jpg"
                        }
                    }
                },
                {
                    "type": "SPONSORED_CONTENT",
                    "post": {
                        "text": "Why sovereign AI matters:\n\n1. No vendor lock-in\n2. Data privacy compliance\n3. Lower long-term costs\n4. Custom hardware optimization\n5. Direct support from the team\n\nFABIABox makes it possible. Pre-order now.\n\n#AI #EdgeComputing #DataPrivacy",
                        "media": {
                            "type": "CAROUSEL",
                            "slides": [
                                {"title": "Sovereign AI", "image": "slide1.jpg"},
                                {"title": "No Lock-in", "image": "slide2.jpg"},
                                {"title": "Custom Hardware", "image": "slide3.jpg"},
                                {"title": "Pre-Order Now", "image": "slide4.jpg"}
                            ]
                        }
                    }
                }
            ],
            "lead_gen_form": [
                {
                    "type": "LEAD_GEN_FORM",
                    "form": {
                        "title": "Pre-Order FABIABox Hardware",
                        "description": "Get priority access to cutting-edge AI hardware. Pre-buy reservation: €500.",
                        "fields": ["full_name", "email", "company", "phone", "product_interest"],
                        "privacy_policy": "https://fabiabox.com/privacy",
                        "thank_you_message": "Thank you for your interest in FABIABox. We'll contact you within 24 hours with pricing and delivery details."
                    }
                }
            ]
        }
        
        return ads
```

### Phase 4: Campaign Optimization

```python
class LinkedInOptimizationAgent:
    def optimize_campaigns(self):
        """Auto-optimize FABIABox LinkedIn campaigns."""
        
        campaigns = self.get_campaign_performance()
        
        for campaign in campaigns:
            # Adjust budget based on performance
            if campaign["cpa"] < 200:
                self.increase_budget(campaign["id"], 25)
                
            elif campaign["cpa"] > 400:
                self.decrease_budget(campaign["id"], 20)
                self.refine_targeting(campaign["id"])
            
            # A/B test ad creatives
            if campaign["ad_creatives"]:
                for creative in campaign["ad_creatives"]:
                    if creative["ctr"] > 0.02:
                        # Scale winning creatives
                        self.increase_budget(campaign["id"], 15)
                    elif creative["ctr"] < 0.005:
                        # Pause underperforming creatives
                        self.pause_ad(campaign["id"], creative["id"])
            
            # Refresh audiences quarterly
            if campaign["days_active"] > 90:
                self.refresh_audiences(campaign["id"])
```

---

## LinkedIn Content Strategy

### Content Types for FABIABox

| Content Type | Purpose | Frequency |
|-------------|---------|-----------|
| Technical deep-dives | Show FABIABox architecture | 2x/week |
| Product announcements | New hardware tiers, features | As needed |
| Customer case studies | Social proof | 1x/month |
| Industry insights | Position as thought leader | 2x/week |
| Behind-the-scenes | Company culture, development | 1x/week |
| Live Q&A / AMA | Community engagement | 1x/month |
| Webinar promotions | Drive registrations | As scheduled |
| Research paper shares | Academic credibility | As published |

### Posting Best Practices

- **Timing:** Tuesday-Thursday, 9-11 AM or 2-4 PM (local time of target audience)
- **Length:** 150-300 words for text posts, longer for articles
- **Media:** Always include images or video — posts with media get 2x engagement
- **Hashtags:** 3-5 relevant hashtags (#SovereignAI, #AIInfrastructure, #EdgeComputing, #AGI, #AIHardware)
- **CTA:** Clear call-to-action in every post
- **Engagement:** Respond to comments within 2 hours

---

## LinkedIn Sales Navigator Integration

### Lead Management

```python
class LinkedInSalesAgent:
    def manage_leads(self):
        """Manage FABIABox leads via LinkedIn Sales Navigator."""
        
        # Identify high-value prospects
        prospects = self.find_prospects(
            job_titles=["CTO", "CIO", "VP of Engineering"],
            industries=["Artificial Intelligence", "Computer Software"],
            company_size="500+",
            geography=["Europe", "North America"]
        )
        
        # Personalize outreach
        for prospect in prospects:
            message = self.generate_personalized_message(
                prospect,
                fabiabox_value="sovereign AI infrastructure"
            )
            self.send_connection_request(prospect, message)
            
            if prospect.accepted:
                self.send_follow_up(prospect, fabiabox_content)
```

---

## Next Steps

1. [ ] Set up LinkedIn Developer account and API access
2. [ ] Create LinkedIn Company Page for FABIABox
3. [ ] Configure OAuth2 credentials
4. [ ] Build initial audiences based on target personas
5. [ ] Create campaigns for each product tier
6. [ ] Set up lead gen forms for pre-order capture
7. [ ] Implement automated optimization
8. [ ] Launch campaigns and begin A/B testing

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
