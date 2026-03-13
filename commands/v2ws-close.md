---
name: v2ws-close
description: "Generate the 6-part close sequence for webinar CTA"
agent: Alessandro (Webinar Architect)
ccp_layer: Expression (L7)
pi_extensions: [SoulResonance]
skills_invoked: [v2ws/close/information, v2ws/close/old-habits, v2ws/close/pain-relief, v2ws/close/do-nothing, v2ws/close/offer, v2ws/close/objections]
---

# v2ws-close

> Generate the complete 6-part close sequence.

## Usage
```
/v2ws-close [webinar_id]
```

## Pipeline (Sequential — each builds on previous)
1. Information Close — dissolve "I need more info" belief
2. Old Habits Close — confront habitual resistance
3. Pain Relief Close — amplify cost of inaction
4. Do Nothing Close — make inaction feel like a choice
5. Offer — present the offer with value stack
6. Close Objections — handle final purchase barriers

## Output
- `close/{webinar_id}_close_sequence.md`
- `close/{webinar_id}_close_slides.json`

## Next Step
Run `/v2ws-render` to compile the final `.excalidraw` deck.
