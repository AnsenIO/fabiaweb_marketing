# FABIABox Marketing Pipeline

Automated, programmatic marketing across all platforms for FABIABox products and services.

## Goal

Build a repeatable, documented pipeline for marketing FABIABox hardware and agentic services across:

- Social media (X/Twitter, LinkedIn, etc.)
- Email campaigns
- Content distribution (blog, research page, SEO)
- Community engagement (Discord, forums, etc.)
- Paid advertising (where applicable)

## Structure

```
fabiaweb_marketing/
├── README.md                    # This file
├── config/
│   ├── marketing.yaml           # Channel config, brand settings, LLM endpoint
│   └── .env.example             # Credential template
├── docs/                        # Strategy and platform playbooks
│   ├── agents/                  # Platform-specific execution guides
│   └── strategy/                # Master, traction, and investor strategies
├── scripts/
│   └── agentic_loop/            # End-to-end autonomous marketing loop
├── templates/                   # Brand voice, content briefs, creative templates
├── literature/                  # Research PDFs
└── data/                        # Campaign data, analytics, metrics
```

## Quick start

1. `cp config/.env.example config/.env` and fill in credentials.
2. `pip install -r requirements.txt`
3. Run a dry-run content generation:
   ```bash
   python -m scripts.agentic_loop.main --angle "founder transformation" --product "Agentic Build Plan"
   ```
4. To actually publish, add `--run` (requires credentials).

## Current Products

### Hardware
| Product | Chip | Price | Reservation |
|---|---|---|---|
| FABIABox Entry | AMD Ryzen AI Max+ | Price on request | €500 |
| FABIABox Edge | NVIDIA Thor | Price on request | €500 |
| FABIABox Pro | NVIDIA DGX Spark (1 PFlop) | Price on request | €500 |
| FABIABox Enterprise | NVIDIA DGX roadmap (20 PFlop) | Price on request | €500 |

### Services
| Plan | Description | Pricing |
|---|---|---|
| Agentic Build Plan | From idea to launched product | €49.99/mo or €499/yr |
| Agentic Operate Plan | Operate, market, optimize | €49.99/mo or €499/yr |

## Status

- [x] Repo cloned under `~/projects/fabiaweb_marketing`
- [x] Dual-track strategy defined (traction + investor)
- [x] Agentic loop skeleton built (Email, X, Discord, Meta)
- [ ] Platform credentials configured
- [ ] Brand assets collection
- [ ] Content calendar setup
- [ ] Social media automation pipeline
- [ ] Email campaign automation
- [ ] Analytics tracking setup

## Strategy docs

| File | Purpose |
|------|---------|
| [docs/strategy/master_strategy.md](docs/strategy/master_strategy.md) | Overall thesis, phases, shared positioning, 90-day roadmap |
| [docs/strategy/traction_strategy.md](docs/strategy/traction_strategy.md) | Drive shop.fabiabox.com interest and purchases |
| [docs/strategy/investor_strategy.md](docs/strategy/investor_strategy.md) | Convert traction into a €500k–€1M Pre-Seed SAFE |
