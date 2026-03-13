---
name: "Distribution Orchestrator"
description: "Automates social + visual generation for all AUTHORIZED scripts"
session_id: ccf-distribute
phase: distribution
ccp_layer: Orchestration (L5)
pi_extensions: [TeamOrchestrator]
inputs:
  - config.yaml
  - All AUTHORIZED scripts from validation/verdicts/
outputs:
  - distribution/{blueprint_id}_tweets.json (per script)
  - distribution/{blueprint_id}_captions.json (per script)
  - visuals/recipes/{blueprint_id}_{recipe}_visual_prompt.md (per script)
  - distribution/manifest.json (summary of all outputs)
depends_on: [story-6.1, story-6.2]
---

# Distribution Orchestrator — ccf-distribute

## Purpose
Automates the complete distribution asset generation for all AUTHORIZED scripts in a batch.
After validation (Epic 5), each AUTHORIZED script needs social content and visual recipes applied.

## Execution Flow

### Step 1: Discover AUTHORIZED Scripts
```
Read config.yaml -> find all scripts with validation status = "AUTHORIZED"
Skip any REJECTED or PENDING scripts
Log: "Found N AUTHORIZED scripts for distribution"
```

### Step 2: For Each AUTHORIZED Script (Parallel)
```
For each blueprint_id with AUTHORIZED status:
  
  A) Smart Mix Synthesis (Story 6.1)
     -> Load scripts/final/{blueprint_id}_script.md
     -> Execute smart-mix/SKILL.md
     -> Output: distribution/{blueprint_id}_tweets.json
     -> Output: distribution/{blueprint_id}_captions.json
     -> Output: distribution/{blueprint_id}_quote_cards.json
  
  B) Art Direction + Visual Recipe (Story 6.2)
     -> Load scripts/final/{blueprint_id}_script.md
     -> Read script's `archetype_metadata.visual_category` (single_frame, comparison, sequential, instructional)
     -> Execute art-director/SKILL.md to select specific recipe within that category
     -> Execute visual-recipes/{selected_recipe}/SKILL.md
     -> Output: visuals/recipes/{blueprint_id}_{recipe}_visual_prompt.md
```

### Step 3: Generate Distribution Manifest
```json
{
  "batch_id": "...",
  "timestamp": "...",
  "scripts_processed": N,
  "outputs": {
    "{blueprint_id}": {
      "tweets": "distribution/{blueprint_id}_tweets.json",
      "captions": "distribution/{blueprint_id}_captions.json",
      "quote_cards": "distribution/{blueprint_id}_quote_cards.json",
      "visual_prompt": "visuals/recipes/{blueprint_id}_{recipe}_visual_prompt.md",
      "art_direction": "visuals/{blueprint_id}_art_direction.json"
    }
  }
}
```

### Step 4: Checkpoint
```
Update config.yaml: sessions.distribution.status = "complete"
Save distribution/manifest.json
```

## I-R-E-V-C Session Protocol

### INGEST
- Load config.yaml
- Identify all AUTHORIZED scripts

### REASON
- For each AUTHORIZED script, determine distribution requirements
- Select appropriate visual recipe via Art Director

### EMIT
- Execute Smart Mix + Visual Recipe for each script
- Generate distribution/manifest.json

### VALIDATE
- All AUTHORIZED scripts have distribution outputs
- manifest.json is complete and accurate
- Only AUTHORIZED scripts processed (REJECTED skipped)

### CHECKPOINT
- Update config.yaml: sessions.distribution.status = "complete"
