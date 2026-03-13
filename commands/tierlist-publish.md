---
name: tierlist-publish
description: "Export .excalidraw tierlist to PNG and prepare for distribution"
agent: Grant (Render Controller)
ccp_layer: Expression (L7)
pi_extensions: [TillDone]
---

# tierlist-publish

> Export a completed tierlist from `.excalidraw` to distribution-ready PNG.

## Usage
```
/tierlist-publish [tierlist_id]
```

## Pipeline
1. Load `.excalidraw` file for the tierlist
2. Export as high-resolution PNG
3. Generate social media caption from reasoning
4. Package for distribution (PNG + caption + metadata)

## Output
- `tierlists/{tierlist_id}.png` (high-res export)
- `tierlists/{tierlist_id}_caption.md` (social media ready)
- `tierlists/{tierlist_id}_metadata.json` (dimensions, file size, export settings)
