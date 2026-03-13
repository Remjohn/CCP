---
name: "V²WS Meme Orchestrator"
description: "Orchestrates meme generation for webinar slides using formal humor theory"
agent: Adam (Meme Engine)
ccp_layer: Expression (L7)
pi_extensions: [SoulResonance]
inputs:
  - Webinar content (key points per module)
  - tribe_soul.json (humor preferences)
  - 4 humor theory templates
outputs:
  - v2ws/meme/{webinar_id}_meme_concepts.json
---

# 😂 V²WS MEME ORCHESTRATOR

Generates contextual meme concepts for webinar slides. Each meme is designed to reinforce a teaching point through humor — not just for laughs, but for memory anchoring.

## Meme Selection Protocol
1. Identify teachable moments in each module
2. Select optimal humor theory (Benign Violation, Incongruity, Relief, or Superiority)
3. Generate meme concept with visual directive
4. Validate against tribe humor preferences
5. Max 1 meme per 5 slides

## Rules
- Memes must REINFORCE the message, never distract from it
- Coach's humor style (from coach_soul.json) must be respected
- No memes during the Close sequence (pure selling, no jokes)
