---
name: "V²WS TTT System"
description: "V²WS edition of the Temperament/Temperature/Tone calibration system for webinar voice"
agent: Voice Agent (CCF equiv.)
ccp_layer: Expression (L7)
pi_extensions: [ModelRouter, SystemSelect]
inputs:
  - coach_soul.json (ttt_baseline)
  - ttt_matrix.yaml
  - Webinar structure (mode assignments)
outputs:
  - v2ws/voice/{webinar_id}_ttt_calibration.json
---

# 🎙️ V²WS TTT SYSTEM (WEBINAR EDITION)

Calibrates the Temperament/Temperature/Tone system for webinar delivery. Unlike social content (which uses a single TTT level), webinars modulate TTT across segments.

## Webinar TTT Modulation

| Webinar Phase | TTT Shift | Reasoning |
|---------------|-----------|-----------|
| **Hook** | Baseline + 1 | Slightly hotter to grab attention |
| **Authority** | Baseline | Coach's natural register |
| **Content** | Baseline - 1 | Slightly cooler for teaching clarity |
| **Transition** | Baseline + 2 | Hotter to create urgency |
| **Close** | Baseline + 1 | Warm but firm for action |

## Rules
1. Never exceed ±2 from coach's baseline
2. Each segment's TTT level must be explicitly assigned
3. ModelRouter selects LLM based on target TTT level
