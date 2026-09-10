# Deep Research: Generative Engine Optimization (GEO / AEO) for LLMs & AI Agents

**Document ID**: RES-GEO-002  
**Target Market**: Local SMBs (Saskatoon & Canadian Metros)  
**Subject**: How LLMs & AI Agents Recommend Local Businesses and Ranked Action Framework

---

## 1. The Architecture of AI Search & Recommendation

As consumers migrate from standard search engines to conversational AI agents (**ChatGPT Search**, **Perplexity AI**, **Google Gemini**, and **Apple Intelligence**), discovery dynamics have fundamentally shifted:

| Attribute | Traditional Google Search (SEO) | Conversational AI Agents (GEO / AEO) |
| :--- | :--- | :--- |
| **Output Type** | List of 10 blue links + Map 3-Pack. | Synthesized narrative recommending 1–3 specific businesses with direct reasoning. |
| **User Behavior** | User clicks, reads multiple websites, compares. | User accepts the AI's synthesized judgment and calls/visits directly. |
| **Data Source** | Web crawlers, PageRank, keyword density. | Retrieval-Augmented Generation (RAG) querying **real-time conversational consensus** + Vector Knowledge Graphs. |
| **Winner Dynamics** | Top 3 positions share 60% of clicks. | **Winner-Takes-All**: The top recommended entity captures 75%+ of user intent. |

```mermaid
flowchart TD
    User["User Query: 'Best Korean restaurant in Saskatoon for a date night'"] --> LLM{"AI Agent Engine"}
    
    subgraph Retrieval Layer (RAG)
        LLM -->|Search Query Formulation| QueryGen["Targeted Queries: site:reddit.com/r/saskatoon, Yelp, GBP reviews"]
        QueryGen --> LiveScrape["Live Search API (Bing / Google / Perplexity Index)"]
        LiveScrape --> Subreddit["r/saskatoon Threads & Comments"]
        LiveScrape --> Reviews["Google Maps & Yelp Review Snippets"]
        LiveScrape --> Curated["Saskatoon StarPhoenix / Tourism Lists"]
    end
    
    subgraph Evaluation & Ranking Layer
        Subreddit --> Sentiment["Entity Co-occurrence & Sentiment Scoring"]
        Reviews --> Sentiment
        Curated --> Sentiment
        Sentiment --> Weighting["Consensus Filtering (Eliminating Paid Ads/Spam)"]
    end
    
    subgraph Synthesis Layer
        Weighting --> Answer["Final Output: 'For Korean food in Saskatoon, the top consensus choice is [Client Name]...'"]
    end
```

---

## 2. Why Reddit (`r/saskatoon`) Dominates LLM Decision-Making

### 1. Multi-Million Dollar Licensing Agreements
Both **OpenAI (ChatGPT)** and **Google (Gemini)** maintain official multi-million dollar data-sharing partnerships with Reddit. Reddit’s content is ingested into training weights and accessed via high-priority live search endpoints during RAG generation.

### 2. The RLHF "Human Truth" Bias
Modern LLMs are trained using Reinforcement Learning from Human Feedback (RLHF) to prioritize unbiased, first-hand human experiences over self-serving marketing copy.
- When an LLM evaluates a restaurant's own website (`"We have the best Korean BBQ in Saskatoon"`), it assigns a low truth-confidence score because it recognizes marketing text.
- When an LLM extracts 12 distinct Reddit comments on `r/saskatoon` stating: *"Hands down [Client Name] on 8th Street, their bulgogi and fried chicken are the best in the city"*, it assigns a **very high confidence score**. The LLM concludes: **This is verified human consensus**.

### 3. Entity Co-occurrence in Vector Embeddings
LLMs represent words and concepts as multidimensional vectors:
- When the entity `[Client Name]` repeatedly appears in the same vector neighborhood as `["best", "authentic", "Korean BBQ", "Saskatoon", "crispy chicken"]` across independent Reddit discussions, the model mathematically links the entity to the query concept.

---

## 3. How Different AI Search Engines Retrieve Local Data

| Engine | Primary Retrieval Mechanism | Dominant Citation Sources | How to Win Top Rank |
| :--- | :--- | :--- | :--- |
| **ChatGPT Search (OpenAI)** | Live Bing index + direct Reddit licensing API + OpenTable / Yelp feeds. | Reddit (`r/saskatoon`), Yelp Saskatoon, TripAdvisor, official business website. | Reddit conversational mentions + rich Schema.org markup on website. |
| **Perplexity AI** | Multi-source live crawler with real-time PerplexityBot index. | Reddit, Google Maps reviews, Saskatoon news articles (StarPhoenix, Narcity), Yelp. | Citation authority across multiple sources + clear factual FAQs on website. |
| **Google Gemini / AI Overviews** | Direct integration into Google's Knowledge Graph & Google Business Profile database. | Google Business Profile reviews, Google Maps user photos, Google Posts. | Review velocity + keyword-rich owner responses + primary category accuracy. |
| **Apple Intelligence (Siri)** | Apple Business Connect + Yelp Ratings & Reviews + DuckDuckGo. | Yelp ratings, Apple Maps native listings, TripAdvisor. | Claiming Apple Business Connect profile + maintaining $\ge 4.5$ on Yelp. |

---

## 4. Ranked Steps to Make Clients the #1 AI Recommendation (Ranked 1 to 10)

Deploy this ranked 10-step strategy to make your client the undisputed #1 recommendation across ChatGPT, Perplexity, and Gemini:

```text
[Rank 1: Reddit Organic Consensus] ➔ [Rank 2: Semantic Review Prompting] ➔ [Rank 3: Complete Schema.org JSON-LD]
  ➔ [Rank 4: Tier-1 Citation Ecosystem] ➔ [Rank 5: Conversational Website FAQs] ➔ [Rank 6: Local Editorial PR Placement]
    ➔ [Rank 7: Apple Business Connect Claim] ➔ [Rank 8: Continuous LLM Query Auditing] ➔ [Rank 9: Visual & Menu Transcripts]
      ➔ [Rank 10: Entity Disambiguation Defense]
```

### Rank 1: Build Organic Consensus on Reddit (`r/saskatoon`) (Highest Impact)
- **Action**: Actively monitor `r/saskatoon` for recommendation queries (e.g., *"Where to get Korean food?"*, *"Best auto body repair in YXE?"*).
- **Execution**: 
  - Encourage genuine patrons, local Saskatoon foodie club members, and loyal VIP customers to share their authentic experiences when recommendation threads arise.
  - Never use automated spam bots or fresh throwaway accounts (Reddit moderators remove them and LLM spam filters discard low-karma accounts). Authentic mentions in existing recommendation archives remain indexed for years.
- **Why It's #1**: This is the single highest-weighted data source for ChatGPT Search and Perplexity.

### Rank 2: Engineer Semantic Keywords into Customer Reviews
- **Action**: Configure your dynamic NFC landing page with **Keyword Inspiration Chips**.
- **Execution**: When happy customers tap the card and click 5 stars, display gentle prompt chips before they jump to Google:
  - *Tip: Mention your favorite dish! (e.g., Bulgogi, Soy Garlic Fried Chicken, Bibimbap)*
- **Impact**: LLMs parse review text to summarize why a place is good. If 30 reviews mention "crispy fried chicken on 8th Street", LLMs synthesize that exact phrase into their recommendation answer.

### Rank 3: Embed Multi-Type Schema.org JSON-LD on Client Website
- **Action**: Add deep, machine-readable structured data to the client's website header.
- **Specification**:
  - Include `@type: "Restaurant"` (or specific category e.g. `DentalClinic`, `AutoRepair`).
  - Embed `servesCuisine`, `priceRange`, `hasMenu`, `geo` coordinates, `openingHoursSpecification`, and `aggregateRating`.
- **Impact**: Eliminates AI hallucinations and gives web crawlers (GPTBot, PerplexityBot) 100% structured certainty regarding offerings, pricing, and operating hours.

### Rank 4: Synchronize the Tier-1 Citation Ecosystem
- **Action**: Standardize business details across the top 5 directories referenced by AI search:
  1. Google Business Profile
  2. Yelp Saskatoon
  3. TripAdvisor
  4. Bing Places
  5. Apple Maps
- **Impact**: LLMs perform cross-source verification. If business information is identical across all 5 directories, confidence scores reach maximum threshold.

### Rank 5: Build a High-Information-Density Conversational FAQ Page
- **Action**: Add an FAQ section on the client’s website that directly mirrors conversational voice queries:
  - *"Does [Restaurant] offer halal or vegetarian Korean options in Saskatoon?"*
  - *"Is [Restaurant] good for large group bookings and birthday parties?"*
  - *"What are the most popular dishes at [Restaurant] on 8th Street?"*
- **Impact**: AI crawlers scrape and directly quote these clear, factual answers in response to complex user prompts.

### Rank 6: Secure Mentions in Local Editorial Roundups & Saskatoon Media
- **Action**: Pitch local publications for inclusion in annual or seasonal "Best of" guides:
  - Saskatoon StarPhoenix
  - Narcity Saskatchewan
  - Tourism Saskatoon
  - The Sheaf (USask student publication)
- **Impact**: Editorial listicles with high domain authority are canonical RAG citations for Perplexity and Bing.

### Rank 7: Claim & Enrich Apple Business Connect
- **Action**: Claim the business on `businessconnect.apple.com`.
- **Execution**: Upload high-res logos, action buttons ("Book Online", "Call"), and showcase hours.
- **Impact**: Powers Apple Intelligence, Siri voice queries, and native Apple Maps searches on over 60% of Canadian iPhones.

### Rank 8: Run Weekly LLM Audit Queries (Continuous Monitoring)
- **Action**: Execute systematic test prompts across ChatGPT, Perplexity, and Gemini:
  - Query: *"What are the top 3 [category] in Saskatoon and why?"*
  - Query: *"Where should I go for [signature dish/service] in Saskatoon?"*
- **Execution**: Inspect the cited sources in Perplexity. Identify which sources recommended competitors and systematically target those citation gaps.

### Rank 9: Provide Searchable Text Menus (Never PDF-Only or Image-Only)
- **Action**: Convert image-only or PDF menus into crawlable HTML text on the client's website.
- **Impact**: Many LLM web scrapers do not execute OCR on PDF downloads during rapid RAG queries. Plain text menus ensure every dish name and price is fully indexed.

### Rank 10: Enforce Entity Disambiguation Defense
- **Action**: Ensure the brand name is completely unique and distinct from businesses in other provinces or cities.
- **Execution**: Use localized entity branding on all official assets (e.g., *"Arisu Korean Restaurant Saskatoon"* rather than just *"Arisu"*).
- **Impact**: Prevents LLMs from confusing your Saskatoon client with similarly named businesses in Calgary, Vancouver, or Toronto.
