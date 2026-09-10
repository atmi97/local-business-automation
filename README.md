# Local Business Automation: Saskatoon Market Launch & SaaS Engine

A turnkey business-in-a-box for launching a local business review & reputation agency in Saskatoon, Saskatchewan. Built using Alex Hormozi's *$100M Offers*, *$100M Leads*, and *$100M Money Models* frameworks to transition from high-margin physical NFC hardware ($97 CAD) into recurring B2B software subscriptions ($97–$297/mo).

---

## 📋 Master Execution Plan
- 🎯 **[TODO.md](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/TODO.md)**: Master prioritized action plan (Phase 1 through Phase 6) to go from \$0 to your first 5 paying Saskatoon clients and ascend them to monthly software continuity.

---

## 📚 Complete Documentation & Deep Research

| Document | Purpose |
| :--- | :--- |
| 📦 [01. Hardware Sourcing Guide](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/01_sourcing_guide.md) | How to buy NTAG215/216 chips in Canada within 24–48h for <$3/unit, local Saskatoon print shops, and AliExpress/Alibaba wholesale scaling. |
| 🎯 [02. Saskatoon Sales Playbook](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/02_sales_playbook_saskatoon.md) | Hormozi Grand Slam Offer, 90-second walk-in script, 8th Street / Broadway / Downtown targeting, and objection handling matrix. |
| 📱 [03. NFC Hardware Setup Guide](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/03_nfc_hardware_setup_guide.md) | How to extract direct Google review links, program NFC chips with free mobile apps, and why dynamic redirect URLs are essential. |
| 🔍 [04. Deep Research: Local SEO Ranking Factors (10 Ranked Steps)](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/04_deep_research_local_seo_ranking_factors.md) | Exhaustive research into Google Local Pack ranking signals, review velocity and decay, how owner review replies inject NLP entity keywords, algorithm update frequency, and **10 ranked steps to keep clients ranking high**. |
| 🤖 [05. Deep Research: Generative Engine Optimization (GEO) (10 Ranked Steps)](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/05_deep_research_geo_aeo_llm_search.md) | Exhaustive research on how LLMs (ChatGPT Search, Gemini, Perplexity) recommend local businesses, why Reddit (`r/saskatoon`) is the #1 consensus source, Schema markup, and **10 ranked steps to make clients the #1 AI recommendation**. |
| 🛠️ [Platform Technical Specifications](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/platform_spec.md) | Complete SaaS architecture, database DDL schema (PostgreSQL), GBP API integration, and review gating compliance rules. |

---

## 🎨 Templates & Prospecting Data

| Asset | Location |
| :--- | :--- |
| 📍 **Curated Saskatoon Prospect Database** | [data/saskatoon_targets.json](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/data/saskatoon_targets.json) (Target profiles across 8th St, Broadway, Downtown with customized pitch angles) |
| 🖨️ **Print Specs & Production Guide** | [templates/card_and_stand_templates.md](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/templates/card_and_stand_templates.md) (Dimensions, colors, bleed specs for Minuteman Press / Staples) |
| 🖼️ **Vector NFC Sticker Artwork (SVG)** | [templates/nfc_sticker_template.svg](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/templates/nfc_sticker_template.svg) (High-contrast, print-ready vector template) |
| 📝 **Client Agreement & Hormozi Guarantee** | [templates/client_service_agreement_template.md](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/templates/client_service_agreement_template.md) (30-day money-back guarantee contract) |

---

## 💻 Working CLI & Software Tools

Run CLI commands directly in your terminal:

```bash
# 1. Generate Direct Google & Dynamic NFC URLs
python src/cli.py generate-link --place-id "ChIJ3V8eYnTYBFMR8o9V29xZ1-E" --slug "saskatoon-korean-bbq"

# 2. Test the AI Local SEO Review Responder
python src/cli.py test-reply --business "Arisu Korean BBQ" --stars 5 --reviewer "Marcus" --comment "Crispy fried chicken was incredible!"

# 3. Generate Machine-Readable Schema.org JSON-LD for AI Crawlers
python src/cli.py generate-schema --business "Arisu Korean BBQ" --category "Restaurant" --address "1505 8th St E" --city "Saskatoon" --rating 4.8 --reviews 285

# 4. Launch Dynamic Redirect & Sentiment Funnel Server
python src/cli.py serve --port 8000
```

---

## 🧪 Automated Testing
Run the complete test suite:
```bash
python -m pytest tests/ -v
```
*(17 passing tests validating link construction, NFC capacity limits, sentiment classification, SEO injection, web funnel routing, and Schema auditing).*
