# Email Marketing — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage email marketing for FABIABox pre-orders, nurturing, and campaigns.

---

## Email Platform Options

### Recommended: Mailtrain (Self-Hosted)

| Aspect | Details |
|--------|---------|
| URL | [Mailtrain](https://github.com/Mailtrain-org/mailtrain) |
| Type | Open-source newsletter app |
| Stars | 5.7k |
| Cost | Free (self-hosted) |
| API | REST API available |
| Integration | Can run on gx10 or FABIABox infrastructure |

### Alternative: Mautic (Open-Source)

| Aspect | Details |
|--------|---------|
| URL | [Mautic](https://github.com/mautic/mautic) |
| Type | Open-source marketing automation |
| Stars | 10.1k |
| Cost | Free (self-hosted) |
| API | REST API available |
| Features | Lead management, campaigns, automation |

### Alternative: SendGrid / Postmark (SaaS)

| Aspect | Details |
|--------|---------|
| SendGrid | [SendGrid](https://sendgrid.com/) — $14.95/mo |
| Postmark | [Postmark](https://postmarkapp.com/) — $15/mo |
| Type | Transactional + marketing email |
| API | REST API available |
| Features | High deliverability, analytics |

---

## Mailtrain MCP Server Setup

```bash
# Install Mailtrain MCP server
npm install @mailtrain/marketing-mcp-server

# Configure
export MAILTRAIN_URL="https://mailtrain.fabiabox.com"
export MAILTRAIN_API_KEY="your_api_key"
export MAILTRAIN_LIST_ID="your_list_id"
```

---

## Agent Instructions for Email Marketing

### Phase 1: List Management

```python
class EmailListAgent:
    def manage_lists(self):
        """Manage FABIABox email lists."""
        
        lists = {
            "pre_order_hardware": {
                "name": "FABIABox Hardware Pre-Orders",
                "description": "People who pre-ordered or expressed interest in FABIABox hardware",
                "segments": {
                    "entry": "FABIABox Entry interest",
                    "edge": "FABIABox Edge interest",
                    "pro": "FABIABox Pro interest",
                    "enterprise": "FABIABox Enterprise interest"
                }
            },
            "pre_order_services": {
                "name": "FABIABox Services Pre-Orders",
                "description": "People who pre-ordered or expressed interest in FABIABox services",
                "segments": {
                    "build_plan": "Agentic Build Plan interest",
                    "operate_plan": "Agentic Operate Plan interest"
                }
            },
            "waiting_list": {
                "name": "FABIABox Waiting List",
                "description": "People on the general waiting list"
            },
            "newsletter": {
                "name": "FABIABox Newsletter",
                "description": "General newsletter subscribers"
            },
            "leads": {
                "name": "FABIABox Qualified Leads",
                "description": "Leads that have been qualified and are ready for sales outreach"
            }
        }
        
        return lists
```

### Phase 2: Campaign Sequences

```python
class EmailCampaignAgent:
    def create_sequences(self):
        """Create email sequences for FABIABox."""
        
        sequences = {
            "welcome_sequence": {
                "name": "FABIABox Welcome",
                "trigger": "new subscriber",
                "emails": [
                    {
                        "day": 0,
                        "subject": "Welcome to FABIABox — The AI Co-Founder That Ships Your Company",
                        "content": "Thank you for your interest in FABIABox. Here's what you need to know..."
                    },
                    {
                        "day": 2,
                        "subject": "How FABIABox Works — Sovereign AI Infrastructure",
                        "content": "FABIABox gives you the hardware and agentic services to build your own AI company..."
                    },
                    {
                        "day": 5,
                        "subject": "FABIABox Product Tiers — Find Your Fit",
                        "content": "From Entry to Enterprise, here's how FABIABox can help..."
                    },
                    {
                        "day": 8,
                        "subject": "Pre-Order FABIABox — €500 Reservation",
                        "content": "Pre-buy a FABIABox workstation or subscribe to agentic services..."
                    },
                    {
                        "day": 12,
                        "subject": "Last Chance — FABIABox Pre-Order Opens Soon",
                        "content": "Don't miss out on priority access to cutting-edge AI hardware..."
                    }
                ]
            },
            "hardware_nurture": {
                "name": "FABIABox Hardware Nurture",
                "trigger": "hardware interest",
                "emails": [
                    {
                        "day": 0,
                        "subject": "Your FABIABox Hardware Guide",
                        "content": "Here's everything you need to know about FABIABox hardware..."
                    },
                    {
                        "day": 3,
                        "subject": "FABIABox Entry vs Edge vs Pro — Which is Right for You?",
                        "content": "Comparing FABIABox product tiers..."
                    },
                    {
                        "day": 7,
                        "subject": "FABIABox Enterprise — The Future of AI Infrastructure",
                        "content": "Enterprise-grade AI infrastructure with NVIDIA DGX roadmap..."
                    },
                    {
                        "day": 14,
                        "subject": "FABIABox Pre-Order — Priority Delivery",
                        "content": "Pre-buy reservation: €500. Contact us for pricing..."
                    }
                ]
            },
            "services_nurture": {
                "name": "FABIABox Services Nurture",
                "trigger": "services interest",
                "emails": [
                    {
                        "day": 0,
                        "subject": "Agentic Build Plan — From Idea to Product",
                        "content": "The Agentic Build Plan takes you from idea to launched product..."
                    },
                    {
                        "day": 3,
                        "subject": "Agentic Operate Plan — Keep Your Company Running",
                        "content": "Operate, market, and optimize your product with AI..."
                    },
                    {
                        "day": 7,
                        "subject": "FABIABox Services — €49.99/mo or €499/year",
                        "content": "Affordable AI-powered business services..."
                    },
                    {
                        "day": 14,
                        "subject": "Start Your FABIABox Journey Today",
                        "content": "Join the FABIABox community and build your AI future..."
                    }
                ]
            },
            "re_engagement": {
                "name": "FABIABox Re-engagement",
                "trigger": "inactive 30 days",
                "emails": [
                    {
                        "day": 0,
                        "subject": "We Miss You — FABIABox Updates",
                        "content": "Here's what's new with FABIABox..."
                    },
                    {
                        "day": 7,
                        "subject": "Last Chance — FABIABox Pre-Order Closing Soon",
                        "content": "Don't miss out on priority access..."
                    },
                    {
                        "day": 14,
                        "subject": "Final Notice — FABIABox Pre-Order",
                        "content": "This is your last chance to pre-order FABIABox..."
                    }
                ]
            }
        }
        
        return sequences
```

### Phase 3: Content Generation

```python
class EmailContentAgent:
    def generate_content(self, template, context):
        """Generate email content for FABIABox."""
        
        content = {
            "product_announcement": {
                "subject": f"🚀 New: FABIABox {context['product']} Available for Pre-Order",
                "preview": f"Pre-buy reservation: €500. Price on request.",
                "body": f"""
<h1>FABIABox {context['product']} — Now Available for Pre-Order</h1>

<p>{context['description']}</p>

<h2>Key Features:</h2>
<ul>
{context['features']}
</ul>

<h2>Pricing:</h2>
<p>Price on request</p>
<p>Pre-buy reservation: €500</p>

<h2>Next Steps:</h2>
<p>Contact us for pricing and delivery timeline.</p>

<p><a href="https://shop.fabiabox.com/{context['product']}">Learn More →</a></p>
                """
            },
            "industry_update": {
                "subject": f"AI Infrastructure Update — {context['topic']}",
                "preview": "Latest developments in sovereign AI and FABIABox",
                "body": f"""
<h1>AI Infrastructure Update</h1>

<p>{context['summary']}</p>

<h2>What This Means for FABIABox:</h2>
<p>{context['relevance']}</p>

<p><a href="https://fabiabox.com/research">Read More →</a></p>
                """
            },
            "weekly_newsletter": {
                "subject": "FABIABox Weekly — {context['week']}",
                "preview": "AI industry updates and FABIABox news",
                "body": f"""
<h1>FABIABox Weekly</h1>

<h2>📰 AI Industry News</h2>
{context['industry_news']}

<h2>🔧 FABIABox Updates</h2>
{context['product_updates']}

<h2>📚 Resources</h2>
{context['resources']}

<p><a href="https://fabiabox.com">Visit FABIABox →</a></p>
                """
            }
        }
        
        return content
```

### Phase 4: Analytics & Optimization

```python
class EmailAnalyticsAgent:
    def analyze_performance(self):
        """Analyze FABIABox email campaign performance."""
        
        metrics = {
            "overall": {
                "total_subscribers": self.get_total_subscribers(),
                "active_subscribers": self.get_active_subscribers(),
                "unsubscribe_rate": self.get_unsubscribe_rate(),
                "bounce_rate": self.get_bounce_rate()
            },
            "campaign": {
                "open_rate": self.get_open_rate(),
                "click_through_rate": self.get_ctr(),
                "conversion_rate": self.get_conversion_rate(),
                "revenue_per_email": self.get_rpe()
            },
            "sequence": {
                "completion_rate": self.get_sequence_completion_rate(),
                "drop_off_points": self.get_drop_off_points(),
                "best_performing_email": self.get_best_email()
            }
        }
        
        # Generate insights
        insights = self.generate_insights(metrics)
        
        # Recommend optimizations
        recommendations = self.generate_recommendations(insights)
        
        return metrics, insights, recommendations
```

---

## Email Best Practices

### Deliverability

- [ ] Set up SPF, DKIM, and DMARC records
- [ ] Use a dedicated sending IP for FABIABox
- [ ] Warm up the IP gradually
- [ ] Monitor bounce rates and spam complaints
- [ ] Use double opt-in for new subscribers

### Content

- Keep subject lines under 50 characters
- Use personalization (name, product interest)
- Include clear CTAs
- Mobile-optimize all emails
- A/B test subject lines and content
- Include unsubscribe link in every email

### Segmentation

| Segment | Criteria | Content |
|---------|----------|---------|
| Hardware - Entry | Interested in Entry tier | AMD Ryzen AI Max+ content |
| Hardware - Edge | Interested in Edge tier | NVIDIA Thor content |
| Hardware - Pro | Interested in Pro tier | DGX Spark content |
| Hardware - Enterprise | Interested in Enterprise tier | DGX roadmap content |
| Services - Build | Interested in Build Plan | Agentic Build Plan content |
| Services - Operate | Interested in Operate Plan | Agentic Operate Plan content |
| Waiting List | On waiting list | General FABIABox updates |

---

## Next Steps

1. [ ] Set up Mailtrain instance on gx10 or FABIABox infrastructure
2. [ ] Configure domain authentication (SPF, DKIM, DMARC)
3. [ ] Import existing pre-order and waiting list contacts
4. [ ] Create email sequences (welcome, nurture, re-engagement)
5. [ ] Set up automated triggers based on user behavior
6. [ ] Implement analytics tracking
7. [ ] Launch first campaigns
8. [ ] Begin A/B testing and optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
