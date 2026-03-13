---
name: v2ws-slides
description: "Generate slide content, visual directives, and speaker notes for content modules"
agent: Elene (Slide Composer)
ccp_layer: Expression (L7)
pi_extensions: [TeamOrchestrator]
skills_invoked: [v2ws/content/outcome-framework, v2ws/content/step-transformation, v2ws/visual/hook-architect, v2ws/visual/ttt-hook-integration]
---

# v2ws-slides

> Generate slide decks + visual directives for content modules.

## Usage
```
/v2ws-slides [webinar_id]
```

## Pipeline
1. Elene generates CDO (Clearly Defined Outcome) per step
2. Step Transformation scripts generated per content block
3. Visual Hook Architect creates visual directives
4. TTT × Visual Integration maps temperature to design style
5. All modules processed in parallel via TeamOrchestrator

## Output
- `slides/{webinar_id}_{module}_slides.json` (per module)
- `slides/{webinar_id}_{module}_speaker_notes.md` (per module)
- `slides/{webinar_id}_{module}_visual_directives.md` (per module)

## Next Step
Run `/v2ws-close` to generate the close sequence.
