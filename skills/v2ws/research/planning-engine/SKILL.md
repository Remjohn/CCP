---
name: "V2WS Research Planning Engine"
description: "Plans the research agenda for a webinar topic — what to search, what to validate, what gaps to fill"
agent: Lionel (CCF Research Library Architect)
ccp_layer: Deep Research (L1)
pi_extensions: [InteractComp]
inputs:
  - Webinar topic brief
  - coach_soul.json (niche expertise)
  - tribe_soul.json (audience knowledge level)
outputs:
  - v2ws/research/{webinar_id}_research_plan.json
---

# 🔬 V2WS RESEARCH PLANNING ENGINE

Plans the research agenda: what sources to query, what data to validate, and what knowledge gaps need filling before webinar content generation.

## Research Plan Structure
1. **Core topic queries** — 3-5 primary search queries
2. **Competitor scan** — what existing webinars cover this topic
3. **Data validation** — statistics and claims that need sourcing
4. **Gap analysis** — what the audience doesn't know they don't know
5. **Freshness check** — via InteractComp, ensure data is current
