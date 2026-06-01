---
name: v2ws-research
description: "Execute parallel deep + fresh research for webinar content"
agent: Lionel + Maeva (CCF)
ccp_layer: Deep Research (L1)
pi_extensions: [InteractComp]
skills_invoked: [v2ws/research/planning-engine, v2ws/research/deep-analyst, v2ws/research/fresh-analyst]
---

# v2ws-research

> Execute the research phase for a V2WS webinar.

## Usage
```
/v2ws-research [webinar_id]
```

## Pipeline
1. **Planning Engine** — generates research plan from topic brief
2. **Deep Research** — academic/foundational sources (parallel)
3. **Fresh Research** — trending/social signals (parallel)
4. **Compile** — merge into unified research pack

## Output
- `research/{webinar_id}_research_plan.json`
- `research/{webinar_id}_deep_research.json`
- `research/{webinar_id}_fresh_research.json`
- `research/{webinar_id}_research_pack.json` (merged)

## Next Step
Run `/v2ws-structure` to design the webinar structure.
