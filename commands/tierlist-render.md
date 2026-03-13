---
name: tierlist-render
description: "Generate a tier ranking and compile it into an .excalidraw visual"
agent: Gerard (Rating Engine) + Benjamin (Excalidraw Composer)
ccp_layer: Deep Reasoning (L3) → Expression (L7)
pi_extensions: [SoulResonance, TillDone]
---

# tierlist-render

> Generate a topic tierlist and render it as an `.excalidraw` visual.

## Usage
```
/tierlist-render [topic] [coach_id]
```

## Pipeline
1. Gerard generates criteria-based tier rankings (S/A/B/C/D/F)
2. Grant sources/generates visual assets for each item
3. Benjamin compiles rankings into `.excalidraw` tier grid

## Output
- `tierlists/{tierlist_id}_rankings.json`
- `tierlists/{tierlist_id}_reasoning.md`
- `tierlists/{tierlist_id}.excalidraw`

## Next Step
Run `/tierlist-publish` to export as PNG.
