# Master Launch To-Do List: Local Business Automation (Saskatoon)

This to-do list is organized in prioritized chronological phases to take you from \$0 to your first 5 paying clients in Saskatoon, followed by ascending them to \$149–\$297/month recurring software retainers.

---

## Phase 1: Procurement & Immediate Hardware Assembly (Days 1–2)
- [ ] **Step 1.1: Order Rapid Test Hardware on Amazon.ca**
  - Search: `TimesKey NTAG215 PVC Cards 10-pack` or `NTAG215 Acrylic Stand`.
  - Ensure chip type is **NTAG215** (13.56 MHz, 504 bytes).
  - Total cost: ~$15–$25 CAD (Prime 1-2 day delivery).
- [ ] **Step 1.2: Download Mobile Programming Apps**
  - Install **NFC Tools** (by wakdev) on your iPhone or Android.
- [ ] **Step 1.3: Prepare Same-Day Branding Stickers in Saskatoon**
  - Use the design specs in [`templates/card_and_stand_templates.md`](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/templates/card_and_stand_templates.md).
  - Print 10 high-gloss die-cut vinyl stickers (85.5 mm × 54 mm) at **Minuteman Press** (217 22nd St E, Downtown) or **Staples** (8th St East).
  - Cost: ~$10–$15 CAD total.
- [ ] **Step 1.4: Assemble First 3 Demo Units**
  - Apply vinyl stickers onto the PVC cards or acrylic L-stands.
  - Test adhesion and visual finish.

---

## Phase 2: Prospecting & Route Preparation (Day 2)
- [ ] **Step 2.1: Select Your First Commercial Route in Saskatoon**
  - *Recommended First Route*: **8th Street East** (from Cumberland to Circle Dr) or **Broadway Avenue** (8th St to 19th St).
  - High density of restaurants, barbershops, medspas, and auto shops with on-site owner-operators.
- [ ] **Step 2.2: Load Target Businesses from Prospect Database**
  - Open [`data/saskatoon_targets.json`](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/data/saskatoon_targets.json).
  - Pick 10 target businesses that have a 4.0–4.6 rating with fewer than 150 reviews (the prime high-desire zone).
- [ ] **Step 2.3: Pre-Program 2 Demo Stands with Place IDs**
  - Run the CLI tool:
    ```bash
    python src/cli.py generate-link --place-id "<TARGET_PLACE_ID>" --slug "<TARGET_SLUG>"
    ```
  - Open **NFC Tools** on your phone and write the generated dynamic URL onto your demo stand.

---

## Phase 3: Sales Blitz & Walk-in Execution (Days 3–4)
- [ ] **Step 3.1: Execute 10 In-Person Walk-Ins**
  - Go between 10:00 AM – 11:15 AM or 2:00 PM – 3:30 PM (off-peak hours).
  - Wear clean smart-casual attire. Carry 2 demo stands in hand (not in a backpack).
- [ ] **Step 3.2: Deliver the 90-Second Shock-and-Awe Script**
  - Review script in [`docs/02_sales_playbook_saskatoon.md`](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/02_sales_playbook_saskatoon.md).
  - Have owner wake their phone; tap the stand to their phone.
  - Show how their direct Google review page opens in 1.5 seconds.
- [ ] **Step 3.3: Present the Close**
  - Option A: **$97 CAD Cash/Card** on the spot (keep the hardware today).
  - Option B: **14-Day Zero-Risk Trial** (leave the stand on their counter; sign nothing; pay nothing today).
- [ ] **Step 3.4: Train Front-Desk Staff on the "7-Word Ask"**
  - Give staff the laminated cheat-sheet: *"Did you love everything about today's visit? ... Awesome! Tap your phone right here to let our manager know."*

---

## Phase 4: Customer Onboarding & Dynamic Card Setup (Day 5)
- [ ] **Step 4.1: Record Client Details in Agency Portal**
  - Place ID, Business Name, Owner's Cell Phone (for instant negative feedback SMS alerts), and notification email.
- [ ] **Step 4.2: Activate Dynamic Redirect Routing**
  - Configure whether the client starts on **Direct Mode** (instant Google redirect) or **Sentiment Funnel Mode** (positive to Google, negative to manager).
- [ ] **Step 4.3: Issue Receipt & Guarantee Certificate**
  - Provide client with the 30-day money-back guarantee agreement (`templates/client_service_agreement_template.md`).

---

## Phase 5: Day 7 Check-in & Ascension to Continuity ($149/mo) (Day 7–10)
- [ ] **Step 5.1: Review Tap & Review Analytics**
  - Run:
    ```bash
    python src/cli.py serve --port 8000
    ```
  - Check total taps and new Google reviews collected over the week.
- [ ] **Step 5.2: In-Person / Phone Check-In**
  - *"Hey [Owner], you've collected [X] new 5-star reviews this week! Customers are loving it."*
- [ ] **Step 5.3: Pitch the AI Reputation & Local SEO Retainer**
  - Show them how replying to every review with keywords boosts their rank on Google Maps:
    ```bash
    python src/cli.py test-reply --business "<CLIENT_NAME>" --stars 5 --reviewer "Mark" --comment "<ACTUAL_REVIEW>"
    ```
  - Close on **$149 CAD / month** recurring continuity.

---

## Phase 6: Scaling, Wholesale Procurement & GEO Retainers (Month 1+)
- [ ] **Step 6.1: Order Wholesale Hardware from Alibaba**
  - Order 100 custom UV-printed acrylic stands with your agency branding (~$1.10 CAD / unit).
- [ ] **Step 6.2: Launch Generative Engine Optimization (GEO) Retainers ($297/mo)**
  - Implement Schema.org JSON-LD on client website.
  - Monitor and seed organic citations on `r/saskatoon` and local Saskatoon directories using the ranked framework in [`docs/05_deep_research_geo_aeo_llm_search.md`](file:///c:/Atabak/Anti%20Gravity%20Projects/Local-business-automation/docs/05_deep_research_geo_aeo_llm_search.md).
- [ ] **Step 6.3: Run Automated GBP Review Sync & Multi-Location Scaling**
  - Transition from manual monitoring to the automated background polling worker in the platform.
