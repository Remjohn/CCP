---
name: v2ws-structure
description: "Design full webinar structure with intro and transition modules"
agent: Alessandro (Webinar Architect)
ccp_layer: Orchestration (L5)
pi_extensions: [SoulResonance]
skills_invoked: [v2ws/intro/hook, v2ws/intro/authority, v2ws/intro/hope, v2ws/intro/intrigue, v2ws/intro/micro-commit, v2ws/intro/objections, v2ws/transition/bridge, v2ws/transition/momentum, v2ws/transition/recap]
---

# v2ws-structure

> Design the complete webinar structure — intro (6 modules) + transition (3 modules).

## Usage
```
/v2ws-structure [webinar_id]
```

## Pipeline
1. Alessandro designs macro-structure with T/V/R mode assignments
2. Generate 6 Intro modules sequentially (Hook → Authority → Hope → Intrigue → Micro-Commit → Objections)
3. Generate 3 Transition modules (Bridge → Momentum → Recap)

## Output
- `structure/{webinar_id}_structure.json`
- `structure/{webinar_id}_module_map.md`
- `structure/{webinar_id}_intro_scripts.md`
- `structure/{webinar_id}_transition_scripts.md`

## Next Step
Run `/v2ws-slides` to generate slide content and visual directives.
