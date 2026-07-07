# YouTube — FABIABox Marketing Instructions

> **Purpose:** How to programmatically manage YouTube presence and campaigns for FABIABox.

---

## YouTube API Setup

### Authentication

1. Create a Google Cloud project
2. Enable YouTube Data API v3
3. Generate OAuth2 credentials (service account)
4. Create a YouTube channel for FABIABox
5. Get API key for programmatic access

### MCP Server Setup

```bash
# Install YouTube MCP server
npm install @youtube/marketing-mcp-server

# Configure
export YOUTUBE_API_KEY="your_api_key"
export YOUTUBE_CLIENT_ID="your_client_id"
export YOUTUBE_CLIENT_SECRET="your_client_secret"
export YOUTUBE_REFRESH_TOKEN="your_refresh_token"
```

### Key API Endpoints

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Videos | `/youtube/v3/videos` | GET/POST |
| Playlists | `/youtube/v3/playlists` | GET/POST |
| Channels | `/youtube/v3/channels` | GET |
| Comments | `/youtube/v3/commentThreads` | GET/POST |
| Live chat | `/youtube/v3/liveChatMessages` | GET |
| Analytics | `/youtube/v3/analytics` | GET |
| Search | `/youtube/v3/search` | GET |
| Thumbnails | `/youtube/v3/thumbnails` | POST |

---

## Agent Instructions for YouTube

### Phase 1: Content Strategy

```python
class YouTubeContentAgent:
    def plan_content(self):
        """Plan FABIABox YouTube content strategy."""
        
        content_pillars = {
            "product_demos": {
                "description": "Demonstrate FABIABox products and features",
                "frequency": "2x/week",
                "formats": ["product walkthroughs", "benchmarks", "setup guides"],
                "target_length": "5-15 minutes"
            },
            "technical_deep_dives": {
                "description": "Technical content about FABIABox architecture",
                "frequency": "1x/week",
                "formats": ["architecture explanations", "benchmark comparisons", "technical tutorials"],
                "target_length": "10-30 minutes"
            },
            "customer_stories": {
                "description": "Customer testimonials and case studies",
                "frequency": "1x/month",
                "formats": ["interviews", "case study videos", "before/after stories"],
                "target_length": "5-10 minutes"
            },
            "industry_analysis": {
                "description": "AI industry trends and analysis",
                "frequency": "1x/week",
                "formats": ["market analysis", "technology comparisons", "future predictions"],
                "target_length": "10-20 minutes"
            },
            "shorts": {
                "description": "Short-form content for reach",
                "frequency": "3-5x/week",
                "formats": ["quick tips", "product highlights", "industry news"],
                "target_length": "Under 60 seconds"
            }
        }
        
        return content_pillars
```

### Phase 2: Video Script Generation

```python
class YouTubeScriptAgent:
    def generate_scripts(self, topic, product):
        """Generate YouTube video scripts for FABIABox."""
        
        scripts = {
            "product_demo": {
                "title": f"FABIABox {product} — Complete Product Demo",
                "description": f"Complete walkthrough of FABIABox {product}. See the hardware, benchmarks, and setup process.",
                "structure": [
                    {"section": "Introduction", "duration": "0:00-0:30", "content": "Hook + FABIABox overview"},
                    {"section": "Product Overview", "duration": "0:30-2:00", "content": "Key specs and features"},
                    {"section": "Hardware Walkthrough", "duration": "2:00-5:00", "content": "Physical tour of the unit"},
                    {"section": "Setup Process", "duration": "5:00-8:00", "content": "Step-by-step setup guide"},
                    {"section": "Benchmarks", "duration": "8:00-12:00", "content": "Performance testing results"},
                    {"section": "Conclusion", "duration": "12:00-13:00", "content": "Summary + CTA"}
                ],
                "cta": "Pre-order FABIABox {product} — €500 reservation. Link in description."
            },
            "technical_deep_dive": {
                "title": f"Why Sovereign AI Infrastructure Matters — FABIABox Explained",
                "description": "Deep dive into sovereign AI infrastructure and why FABIABox makes it possible.",
                "structure": [
                    {"section": "The Problem", "duration": "0:00-2:00", "content": "Cloud dependency and vendor lock-in"},
                    {"section": "The Solution", "duration": "2:00-5:00", "content": "Sovereign AI infrastructure concept"},
                    {"section": "FABIABox Architecture", "duration": "5:00-10:00", "content": "How FABIABox delivers sovereign AI"},
                    {"section": "Use Cases", "duration": "10:00-13:00", "content": "Real-world applications"},
                    {"section": "Conclusion", "duration": "13:00-14:00", "content": "Summary + CTA"}
                ],
                "cta": "Learn more about FABIABox at fabiabox.com"
            },
            "short": {
                "title": f"FABIABox {product} in 60 Seconds",
                "description": "Quick overview of FABIABox {product}. #AI #SovereignAI",
                "structure": [
                    {"section": "Hook", "duration": "0:00-0:05", "content": "Grab attention"},
                    {"section": "Product", "duration": "0:05-0:20", "content": "What is FABIABox"},
                    {"section": "Features", "duration": "0:20-0:40", "content": "Key features"},
                    {"section": "CTA", "duration": "0:40-0:55", "content": "Call to action"},
                    {"section": "Outro", "duration": "0:55-1:00", "content": "Brand reminder"}
                ],
                "cta": "Pre-order now — link in bio"
            }
        }
        
        return scripts
```

### Phase 3: Video Production Automation

```python
class YouTubeProductionAgent:
    def produce_video(self, script):
        """Automate FABIABox video production."""
        
        steps = {
            "script_to_speech": {
                "action": "Convert script to audio using TTS",
                "tool": "edge-tts or ElevenLabs",
                "output": "audio.wav"
            },
            "visual_generation": {
                "action": "Generate visuals for each section",
                "tool": "Midjourney / DALL-E / custom renders",
                "output": "images/frame_*.png"
            },
            "video_assembly": {
                "action": "Assemble video from audio and visuals",
                "tool": "FFmpeg",
                "output": "fabiabox-video.mp4"
            },
            "subtitle_generation": {
                "action": "Generate and burn in subtitles",
                "tool": "Whisper or manual SRT",
                "output": "fabiabox-video-subtitles.mp4"
            },
            "thumbnail_generation": {
                "action": "Generate thumbnail image",
                "tool": "Midjourney / DALL-E / Canva API",
                "output": "thumbnail.jpg"
            }
        }
        
        return steps
```

### Phase 4: Upload & SEO

```python
class YouTubeUploadAgent:
    def upload_video(self, video_path, script):
        """Upload and optimize FABIABox YouTube video."""
        
        upload_config = {
            "title": script["title"],
            "description": f"""
{script["description"]}

🔗 Learn more: https://fabiabox.com
🛒 Pre-order: https://shop.fabiabox.com
📧 Contact: andrea@iab.ai

#SovereignAI #AIInfrastructure #EdgeComputing #AGI #AIHardware #FABIABox
            """,
            "tags": ["sovereign AI", "AI infrastructure", "FABIABox", "edge computing", "NVIDIA DGX", "AMD Ryzen AI", "AI hardware", "AGI"],
            "category": "Science & Technology",
            "thumbnail": "thumbnail.jpg",
            "privacy": "public",
            "language": "en",
            "default_audio_language": "en",
            "chapters": [
                {"title": "Introduction", "time": "0:00"},
                {"title": "Product Overview", "time": "0:30"},
                {"title": "Hardware Walkthrough", "time": "2:00"},
                {"title": "Setup Process", "time": "5:00"},
                {"title": "Benchmarks", "time": "8:00"},
                {"title": "Conclusion", "time": "12:00"}
            ],
            "end_screen": {
                "type": "video",
                "video_id": "related_fabiabox_video_id"
            },
            "cards": [
                {"type": "link", "text": "Pre-order FABIABox", "url": "https://shop.fabiabox.com"}
            ]
        }
        
        return upload_config
```

### Phase 5: Engagement & Analytics

```python
class YouTubeEngagementAgent:
    def manage_engagement(self):
        """Manage FABIABox YouTube engagement."""
        
        # Monitor comments
        comments = self.get_comments(video_id="current_video")
        
        for comment in comments:
            if comment["sentiment"] == "positive":
                self.like_comment(comment)
                self.reply(comment, "Thank you for your interest! 🚀")
                
            elif comment["sentiment"] == "neutral":
                self.reply(comment, f"Great question! Here's more info: {response}")
                
            elif comment["sentiment"] == "negative":
                self.reply(comment, f"We appreciate your feedback. Please reach out to us at andrea@iab.ai")
        
        # Monitor analytics
        analytics = self.get_analytics(video_id="current_video")
        
        # Generate insights
        insights = {
            "watch_time": analytics["average_watch_time"],
            "retention": analytics["audience_retention"],
            "click_through_rate": analytics["ctr"],
            "top_traffic_sources": analytics["traffic_sources"],
            "demographics": analytics["demographics"]
        }
        
        return insights
```

---

## YouTube Content Calendar

### Weekly Schedule

| Day | Content Type | Focus |
|-----|-------------|-------|
| Monday | Technical deep-dive | FABIABox architecture |
| Tuesday | Product demo | FABIABox product walkthrough |
| Wednesday | Short | Quick tip or product highlight |
| Thursday | Industry analysis | AI infrastructure trends |
| Friday | Short | Product highlight or news |
| Saturday | Customer story | Testimonial or case study |
| Sunday | Short | Industry news or Q&A |

### SEO Best Practices

- **Titles:** Include target keyword, keep under 60 characters
- **Descriptions:** First 2 lines are critical for CTR, include links
- **Tags:** Mix of broad and specific tags
- **Chapters:** Add timestamps for better navigation
- **End Screens:** Link to other FABIABox videos and shop
- **Cards:** Add links to relevant videos and external sites
- **Subtitles:** Always add subtitles for accessibility and SEO

---

## Next Steps

1. [ ] Set up YouTube channel for FABIABox
2. [ ] Configure YouTube API access
3. [ ] Plan initial content calendar
4. [ ] Set up video production pipeline
5. [ ] Create first batch of videos (product demos, architecture explainers)
6. [ ] Implement automated upload and SEO optimization
7. [ ] Set up engagement monitoring
8. [ ] Launch YouTube Shorts strategy
9. [ ] Begin analytics tracking and optimization

---

*Last updated: 2026-07-07*
*Author: Andrea (IABAI)*
