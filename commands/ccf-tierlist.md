---
description: Generate a Tier List or Rating config and launch the recording studio
---

// turbo-all

# CCF Tier List & Rating Recording Studio

## Overview
This command generates 3 YouTube video ideas, creates a JSON config for the Tier List Recording App, and launches the studio for recording.

## Inputs
- `variant` — archetype variant: `authority`, `controversial`, `red-flag`, `relatable`, `nostalgia`, `outrage`, `validation`
- `niche` — coach's niche (e.g., "dating advice", "fitness", "business")
- `content` — specific topic or content idea (optional, agent will generate if empty)

## Execution

### Step 1: Load Archetype Script
Based on the `variant`, load the matching script prompt:

| Variant | Script Path |
|:--------|:------------|
| `authority` | `ccf-26/intelligence/archetype_prompts/tier_lists/✨ The Authority Tier List Script.md` |
| `controversial` | `ccf-26/intelligence/archetype_prompts/tier_lists/✨The Controversial Tier List Script.md` |
| `red-flag` | `ccf-26/intelligence/archetype_prompts/tier_lists/✨The Red Flag Tier List Script.md` |
| `relatable` | `ccf-26/intelligence/archetype_prompts/tier_lists/✨ The Relatable Tier List Script.md` |
| `nostalgia` | `ccf-26/intelligence/archetype_prompts/reactions/✨ The Nostalgia Reaction Script.md` |
| `outrage` | `ccf-26/intelligence/archetype_prompts/reactions/✨The Outrage Reaction Script.md` |
| `validation` | `ccf-26/intelligence/archetype_prompts/reactions/✨The Validation Reaction Script.md` |

| `authority-rating` | `ccf-26/intelligence/archetype_prompts/ratings/✨ The Authority Rating Script.md` |
| `controversial-rating` | `ccf-26/intelligence/archetype_prompts/ratings/✨The Controversial Rating Script.md` |
| `roast-rating` | `ccf-26/intelligence/archetype_prompts/ratings/✨The Roast Rating Script.md` |
| `relatable-rating` | `ccf-26/intelligence/archetype_prompts/ratings/✨ The Relatable Rating Script.md` |

### Step 2: Generate 3 YouTube Video Ideas
Using the coach's niche and the loaded archetype, generate 3 ideas:

For each idea, provide:
- **Title** (CTR-optimized, e.g. "Best Dating Apps Ranked – TIER LIST")
- **Format** (Tier List or Rating)
- **Items** (6-8 items to evaluate)
- **Criteria** (3-4 evaluation axes)
- **Controversy angle** (what will spark debate)

Present the 3 ideas to the coach. Coach selects one.

### Step 3: Generate Config JSON
Create the JSON config file for the selected idea:

```json
{
  "mode": "tier-list",
  "title": "<Selected video title>",
  "criteria": ["<criterion 1>", "<criterion 2>", ...],
  "tiers": {
    "S": { "label": "<descriptor>", "color": "#FFD700", "items": ["<item>"] },
    "A": { "label": "<descriptor>", "color": "#C0C0C0", "items": ["<item>"] },
    "B": { "label": "<descriptor>", "color": "#CD7F32", "items": [] },
    "C": { "label": "<descriptor>", "color": "#FFEB3B", "items": [] },
    "D": { "label": "<descriptor>", "color": "#FF9800", "items": [] },
    "F": { "label": "<descriptor>", "color": "#F44336", "items": [] }
  },
  "unassigned_items": ["<item 1>", "<item 2>", ...],
  "reaction_video": "",
  "commentary_bullets": ["<bullet 1>", "<bullet 2>", ...]
}
```

For **Rating** mode, use:
```json
{
  "mode": "rating",
  "title": "<title>",
  "rating_subject": "<subject name displayed as headline>",
  "criteria": [...],
  "pros": ["<positive metric 1>", "<positive metric 2>", ...],
  "cons": ["<negative metric 1>", "<negative metric 2>", ...],
  "tiers": {},
  "commentary_bullets": [...],
  "reaction_video": ""
}
```

// turbo
Save the config to `tools/tierlist-app/src/data/session-config.json`

### Step 4: Launch the Studio
// turbo
```powershell
cd tools/tierlist-app && npm run dev
```

The coach opens `http://localhost:5173` to see their pre-loaded Excalidraw board.

### Step 5: Recording Notes
Provide the coach with:
1. 8-minute recording structure (from template)
2. Key talking points per tier/rating level
3. When to play the reaction video
4. CTA text for the end

## Recording Structure (8 minutes)

| Minute | Section | Action |
|:-------|:--------|:-------|
| 0-1 | Hook | State why ranking this matters |
| 1-2 | Criteria | Define evaluation framework |
| 2-6 | Tier/Rating Breakdown | Walk through items one by one |
| 6-7 | Reaction Clip | Play video overlay, react live |
| 7-8 | Recap + CTA | Final summary + controversy bait |
