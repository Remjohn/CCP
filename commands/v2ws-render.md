---
name: v2ws-render
description: "Compile all webinar assets into branded .excalidraw deck with module scripts"
agent: Benjamin (Excalidraw Composer) + Grant (Render Controller)
ccp_layer: Expression (L7)
pi_extensions: [TillDone]
skills_invoked: [excalidraw-composer]
---

# v2ws-render

> Compile the final webinar deck as a branded `.excalidraw` file.

## Usage
```
/v2ws-render [webinar_id]
```

## Pipeline
1. Grant resolves all image assets (logos, stick figures, photos → transparent PNGs)
2. Benjamin compiles slides into `.excalidraw` JSON with brand styling
3. Speaker notes embedded as text layers
4. Module scripts attached as companion document
5. TillDone retries if rendering fails (up to 3 attempts)

## Output
- `decks/{webinar_id}.excalidraw`
- `decks/{webinar_id}_speaker_notes.md`
- `decks/{webinar_id}_full_script.md`
- `decks/{webinar_id}_render_report.json`

## This is the FINAL step of the V2WS pipeline.
