# FABIABox / Fabia OS — Running Design Context

## Terminology

| Term | Working definition | Status |
|------|--------------------|--------|
| **Fabia OS** | A pre-configured sovereign AI appliance OS: Linux-based control plane + packaged agentic system + dedicated business/creation tools. | Draft |
| **Hardware agnostic** | Runs on commercially available AI-capable hardware prepared and configured by IABAI. | Confirmed |
| **FABIABox** | The physical appliance (hardware + Fabia OS) that ships to the customer. | Confirmed |
| **Sovereign AI** | Models, data, agent state, and business records stay on the customer-controlled appliance. | Confirmed |
| **Fabia** | The orchestrating AI co-founder that accesses the packaged tools on the user's behalf. | Confirmed |
| **SquadShelf** | External ecosystem that delivers new pipelines, configurations, and model updates to Fabia OS. | Confirmed |

## Design decisions

| # | Decision | Rationale | Open questions |
|---|----------|-----------|----------------|
| D1 | Fabia OS is a pre-installed appliance stack on Linux. | Ships on commercially available hardware prepared by IABAI. | Which base Linux and install flow? |
| D2 | Hardware tiers: Entry / Pro / Enterprise. | Matches customer size and compute need. | Confirmed below. |
| D3 | Bundled tools are white-labelled/re-branded. | User sees one coherent product, not a toolkit. | Naming conventions? |
| D4 | ERP core = Odoo (no public specifics). | Mature open-source ERP; agents manage it. | Which modules are enabled by default? |
| D5 | RAG + dedicated knowledge system is part of the OS. | Company-specific memory and document intelligence. | Per-project or per-appliance? |
| D6 | Agents receive constant updates from SquadShelf. | New pipelines, configs, prompts delivered centrally. | Update mechanism and pricing? |
| D7 | Pre-orders include lifetime premium support + lifetime ecosystem access. | High-value bundle to drive reservations. | Scope of each? |

## Hardware tiers (confirmed)

| Tier | Target user | Reference hardware | Key characteristics |
|------|-------------|--------------------|---------------------|
| **Entry** | Solopreneur / idea-stage founder | **AMD Ryzen AI Max+ 395** APU | 16 Zen 5 cores (32 threads) up to 5.1 GHz, 55W TDP, Radeon 8060S iGPU (40 CU RDNA 3+), XDNA 2 NPU up to 50 TOPS, up to 128 GB LPDDR5X-8000 (256 GB/s), PCIe 4. |
| **Entry alt** | Edge/automotive form factor | **NVIDIA DRIVE AGX Thor** | Thor-X SoC with Blackwell iGPU, ARM Neoverse V3AE CPU, up to 1,000 INT8 TOPS / 2,000 FP4 TFLOPS, devkit ~350 W. |
| **Pro** | Serious founder / agency | **NVIDIA DGX Spark** (GB10 Grace Blackwell Superchip) | 20-core Arm CPU, 128 GB unified memory, up to 1,000 TOPS / 1 PFLOP FP4, supports models up to 200B params (405B dual), 240 W external PSU, 150 mm cube desktop form factor. |
| **Enterprise** | Lab / corporate venture / scale-up | **NVIDIA DGX Station** (GB300 Grace Blackwell Ultra Desktop Superchip) | 72-core Grace Neoverse V2, 252 GB HBM3e + 496 GB LPDDR5X = 748 GB coherent memory, up to 20 PFLOPS FP4, supports models up to 1T params, 1,600 W, deskside tower. |

## Packaged tool categories (white-label candidates)

| White-label name idea | Category | Under-the-hood candidate | Managed by |
|-----------------------|----------|--------------------------|------------|
| Fabia Knowledge | RAG / knowledge base | Qdrant + local embedding models | Research / memory agents |
| Fabia Memory | Long-term agent memory | SQLite + Qdrant memory collection | Orchestrator |
| Fabia Pipelines | Workflow automation | n8n | Ops agents |
| Fabia Projects | Project management | Plane | PM agents |
| Fabia ERP | Customers, invoices, inventory, bank flow, accounting | Odoo | Finance / ops agents |
| Fabia Studio | Image/video generation and editing | ComfyUI + local diffusion models | Creative agents |
| Fabia Code | Coding environment, QA, containerization | OpenCode / SonarQube / Docker | Coding / QA agents |
| Fabia Research | Market research, literature, auto-improvement | Local knowledge base + web agents | Research agents |
| Fabia Marketing | Copy generation, ad management, social publishing | Meta/LinkedIn/X publishers + copy models | Marketing agents |
| Fabia KPIs | Metrics tracking and improvement suggestions | KPI dashboard + improvement agents | Business manager |
| Fabia Sign | Formal signatures | External e-signature ecosystem | Legal agents |
| Fabia Models | Custom model training / fine-tuning | SquadShelf model ecosystem | Model-training agents |
|| Fabia Intelligence | Market intelligence | External data feeds + ecosystem | Research / strategy agents |

## Pre-order bundle

- **Lifetime premium support**
- **Lifetime SquadShelf ecosystem access** at **Founders** level (premium tier; Platinum may exist later)

## Offer-page visual treatment

- Default: each tier shows a polished product image of the FABIABox hardware + a Fabia OS UI/hero overlay.
- Open: use real product photography vs. brand-aligned 3D renders.

## Open questions

1. What does lifetime premium support cover? Hardware, OS updates, agent tuning, 24/7?
2. Pricing model: hardware cost + monthly Fabia OS/agent subscription?
3. Is the RAG/knowledge system per company/project, or shared across all users on the appliance?
4. Which Odoo modules are enabled by default?
5. Do you have real product photography, or should we generate brand-aligned renders?
