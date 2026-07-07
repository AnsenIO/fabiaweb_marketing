# Google Ads & SEO — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage Google Ads campaigns and SEO for FABIABox products and services.

---

## Google Ads API Setup

### Authentication

1. Create a Google Cloud project
2. Enable Google Ads API
3. Generate OAuth2 credentials (service account)
4. Download the service account JSON key
5. Get a developer token from Google Ads

### MCP Server Setup

```bash
# Install Google Ads MCP server
npm install @google-ads/mcp-server

# Configure
export GOOGLE_ADS_CLIENT_ID="your_client_id"
export GOOGLE_ADS_CLIENT_SECRET="your_client_secret"
export GOOGLE_ADS_DEVELOPER_TOKEN="your_token"
export GOOGLE_ADS_REFRESH_TOKEN="your_refresh_token"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| List campaigns | `/googleads/googleads/v16/{customer_id}/campaigns` | GET |
| Create campaign | `/googleads/googleads/v16/{customer_id}/campaigns` | POST |
| Update campaign | `/googleads/googleads/v16/{customer_id}/campaigns` | PATCH |
| List ad groups | `/googleads/googleads/v16/{parent}/adGroups` | GET |
| Create ad group | `/googleads/googleads/v16/{parent}/adGroups` | POST |
| List ads | `/googleads/googleads/v16/{parent}/ads` | GET |
| Create ads | `/googleads/googleads/v16/{parent}/ads` | POST |
| Keyword plans | `/googleads/googleads/v16/{parent}/keywordPlans` | GET |
| Reports | `/googleads/googleads/v16/{customer_id}/reports` | POST |

---

## Agent Instructions for Google Ads

### Phase 1: Keyword Research

```python
class GoogleAdsKeywordAgent:
    def research_keywords(self):
        """Research keywords for FABIABox products."""
        
        # Core FABIABox keywords
        core_keywords = [
            "AI hardware", "AI workstation", "sovereign AI",
            "edge AI computing", "NVIDIA DGX alternative",
            "AMD Ryzen AI", "AI infrastructure",
            "AI co-founder", "agentic AI services",
            "AI build plan", "AI operate plan"
        ]
        
        # Long-tail keywords
        long_tail = [
            "best AI hardware for startups",
            "sovereign AI infrastructure cost",
            "NVIDIA DGX vs alternatives",
            "AI workstation for small business",
            "agentic AI build service",
            "AI-powered company building",
            "edge computing for AI",
            "AMD Ryzen AI Max+ workstation"
        ]
        
        # Use Google Ads API to get search volume and competition
        keywords = []
        for term in core_keywords + long_tail:
            plan = self.get_keyword_plan(term)
            keywords.append({
                "keyword": term,
                "avg_monthly_searches": plan["avg_monthly_searches"],
                "competition": plan["competition"],
                "top_of_page_bid": plan["top_of_page_bid"]
            })
        
        return sorted(keywords, key=lambda x: x["avg_monthly_searches"], reverse=True)
```

### Phase 2: Campaign Creation

```python
class GoogleAdsCampaignAgent:
    def create_campaigns(self, keywords):
        """Create optimized campaigns for FABIABox."""
        
        campaigns = {
            "hardware_search": {
                "name": "FABIABox Hardware - Search",
                "type": "SEARCH",
                "bidding_strategy": "TARGET_CPA",
                "target_cpa": 500,  # €500 CPA for pre-orders
                "budget": 1000,  # €1000/day
                "keywords": [k for k in keywords if "hardware" in k["keyword"] or "workstation" in k["keyword"]],
                "audiences": ["IT decision makers", "AI engineers", "startup founders"],
                "ad_extensions": ["callout", "structured", "location"]
            },
            "services_search": {
                "name": "FABIABox Services - Search",
                "type": "SEARCH",
                "bidding_strategy": "TARGET_ROAS",
                "target_roas": 400,  # 4x ROAS
                "budget": 500,  # €500/day
                "keywords": [k for k in keywords if "agentic" in k["keyword"] or "build" in k["keyword"] or "operate" in k["keyword"]],
                "audiences": ["entrepreneurs", "tech founders", "AI developers"]
            },
            "display_retarget": {
                "name": "FABIABox - Display Retargeting",
                "type": "DISPLAY",
                "budget": 200,  # €200/day
                "target_audiences": ["website visitors", "pre-order list", "content engagers"]
            }
        }
        
        return campaigns
```

### Phase 3: Ad Copy Generation

```python
class GoogleAdsCopyAgent:
    def generate_ads(self, product_tier):
        """Generate ad copy variants for FABIABox."""
        
        ads = {
            "hardware_search": [
                {
                    "headlines": [
                        "FABIABox AI Hardware — Price on Request",
                        "Sovereign AI Infrastructure — Pre-Order Now",
                        "1 PFlop to 20 PFlop — Scale Your AI"
                    ],
                    "descriptions": [
                        "Pre-buy a FABIABox workstation starting at €500 reservation. Access cutting-edge AI hardware before anyone else.",
                        "From AMD Ryzen AI Max+ to NVIDIA DGX roadmap. Choose your FABIABox tier and build your AI future.",
                        "The AI Co-Founder That Ships Your Company. Pre-order now and get priority delivery."
                    ],
                    "callouts": [
                        "Price on Request",
                        "€500 Pre-buy Reservation",
                        "Priority Delivery",
                        "Dedicated Support"
                    ]
                },
                {
                    "headlines": [
                        "NVIDIA DGX Spark — 1 PFlop AI Power",
                        "FABIABox Pro — AI Research Hardware",
                        "DGX Spark Workstation — Pre-Order"
                    ],
                    "descriptions": [
                        "Get the NVIDIA DGX Spark (1 PFlop) in a FABIABox workstation. Pre-buy reservation: €500.",
                        "FABIABox Pro delivers enterprise AI power at your desk. Pre-order now for priority delivery.",
                        "The next generation of AI research hardware. FABIABox Pro with DGX Spark."
                    ]
                },
                {
                    "headlines": [
                        "FABIABox Enterprise — 20 PFlop AI Power",
                        "NVIDIA DGX Roadmap — Enterprise AI",
                        "Scale Your AI — FABIABox Enterprise"
                    ],
                    "descriptions": [
                        "The NVIDIA DGX roadmap (20 PFlop) in a FABIABox Enterprise solution. Pre-buy reservation: €500.",
                        "Enterprise-grade AI infrastructure. FABIABox Enterprise with DGX roadmap access.",
                        "Build your AI future with FABIABox Enterprise. Contact us for pricing."
                    ]
                }
            ],
            "services_search": [
                {
                    "headlines": [
                        "Agentic Build Plan — €49.99/mo",
                        "From Idea to Product — FABIABox",
                        "AI-Powered Build Service"
                    ],
                    "descriptions": [
                        "From idea to launched product. Agentic Build Plan from €49.99/mo or €499/year.",
                        "Let AI build your company. FABIABox Agentic Build Plan handles everything.",
                        "Launch your AI-powered company with FABIABox. Start from €49.99/mo."
                    ]
                },
                {
                    "headlines": [
                        "Agentic Operate Plan — €49.99/mo",
                        "Operate & Optimize — FABIABox",
                        "AI-Powered Business Operations"
                    ],
                    "descriptions": [
                        "Operate, market, and optimize your product. Agentic Operate Plan from €49.99/mo.",
                        "Keep your company running with FABIABox Agentic Operate Plan. €49.99/mo.",
                        "AI-powered business operations. FABIABox Operate Plan handles the hard work."
                    ]
                }
            ]
        }
        
        return ads
```

### Phase 4: Campaign Optimization

```python
class GoogleAdsOptimizationAgent:
    def optimize_campaigns(self):
        """Auto-optimize FABIABox Google Ads campaigns."""
        
        # Get campaign performance data
        campaigns = self.get_campaign_performance()
        
        for campaign in campaigns:
            if campaign["roas"] > 4.0:
                # Scale winning campaigns
                self.increase_budget(campaign["id"], 20)
                self.add_audience_signals(campaign["id"])
                
            elif campaign["cpa"] > 600:
                # Reduce spend on underperformers
                self.decrease_budget(campaign["id"], 15)
                self.refine_targeting(campaign["id"])
                
            # Auto-pause keywords with high cost/low conversion
            keywords = self.get_keyword_performance(campaign["id"])
            for kw in keywords:
                if kw["cost"] > 200 and kw["conversions"] == 0:
                    self.pause_keyword(campaign["id"], kw["id"])
                
                elif kw["roas"] > 5.0:
                    self.increase_bid(campaign["id"], kw["id"], 25)
```

---

## SEO Strategy for FABIABox

### Keyword Strategy

| Category | Target Keywords | Content Type |
|----------|----------------|--------------|
| Product | "AI workstation", "sovereign AI hardware", "edge AI computing" | Product pages, comparison pages |
| Service | "agentic AI build", "AI company building service", "AI operate plan" | Service pages, case studies |
| Technical | "NVIDIA DGX Spark", "AMD Ryzen AI Max+", "NVIDIA Thor" | Technical docs, benchmark reports |
| Industry | "sovereign AI", "AI infrastructure", "AI co-founder" | Blog posts, white papers |
| Comparison | "FABIABox vs NVIDIA", "FABIABox vs cloud AI" | Comparison pages, ROI calculators |

### Technical SEO Checklist

- [ ] Schema markup for products (FAQ, Product, Organization)
- [ ] XML sitemap with all product pages
- [ ] robots.txt configured correctly
- [ ] Canonical URLs set for all pages
- [ ] Mobile-first design verified
- [ ] Core Web Vitals optimized (LCP < 2.5s, CLS < 0.1, INP < 200ms)
- [ ] HTTPS enforced
- [ ] Structured data for pricing (where applicable)
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags for social sharing

### Content SEO Agent

```python
class SEOAuditAgent:
    def audit_website(self):
        """Audit fabiabox.com for SEO issues."""
        
        issues = []
        
        # Check technical SEO
        issues.extend(self.check_technical_seo())
        
        # Check on-page SEO
        issues.extend(self.check_on_page_seo())
        
        # Check content quality
        issues.extend(self.check_content_quality())
        
        # Check backlinks
        issues.extend(self.check_backlinks())
        
        # Generate report
        return self.generate_report(issues)
    
    def optimize_content(self, page):
        """Optimize page content for target keywords."""
        
        # Analyze current content
        current = self.analyze_content(page)
        
        # Generate optimized content
        optimized = self.generate_optimized_content(
            current,
            target_keywords=page.target_keywords,
            competitor_analysis=page.competitor_analysis
        )
        
        # Apply optimizations
        page.title = optimized.title
        page.meta_description = optimized.meta_description
        page.content = optimized.content
        page.schema = optimized.schema
        
        return page
```

---

## Google Analytics Integration

### Event Tracking Setup

```python
class AnalyticsAgent:
    def track_events(self):
        """Set up GA4 event tracking for FABIABox."""
        
        events = {
            "pre_order_click": {
                "category": "Hardware",
                "action": "Pre-order Click",
                "label": "FABIABox Entry|Edge|Pro|Enterprise"
            },
            "product_select": {
                "category": "Hardware",
                "action": "Product Select",
                "label": "FABIABox Entry|Edge|Pro|Enterprise"
            },
            "form_submit": {
                "category": "Lead",
                "action": "Pre-order Form Submit",
                "label": "pre-order"
            },
            "waiting_list_join": {
                "category": "Lead",
                "action": "Waiting List Join",
                "label": "waiting-list"
            },
            "research_click": {
                "category": "Content",
                "action": "Research Page Click",
                "label": "research"
            },
            "pricing_inquiry": {
                "category": "Lead",
                "action": "Price on Request Click",
                "label": "pricing"
            }
        }
        
        return events
```

---

## Next Steps

1. [ ] Set up Google Ads account and developer token
2. [ ] Configure OAuth2 credentials
3. [ ] Create initial campaigns with researched keywords
4. [ ] Set up GA4 tracking for all FABIABox events
5. [ ] Implement SEO audit and optimization
6. [ ] Set up automated reporting
7. [ ] Launch campaigns and begin optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
