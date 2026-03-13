---
name: "Multi-Theme Batch Orchestrator"
description: "Runs content batches across multiple themes, scaling from N to N x T pieces"
session_id: ccf-multi-theme
phase: orchestration
ccp_layer: Orchestration (L5)
pi_extensions: [MemoryFolder, TeamOrchestrator]
inputs:
  - config.yaml
  - intelligence/themes/content_themes.json
outputs:
  - All outputs from ccf-batch x number of themes
  - multi_theme_report.json
depends_on: [story-7.2]
---

# ccf-multi-theme — Multi-Theme Batch Orchestrator

## Purpose
Scale content production across multiple themes. Each theme generates 12 blueprints through `ccf-batch`, producing T x 12 total content pieces.

## Usage
```
ccf-multi-theme --project <path> --themes <theme_id_1> <theme_id_2> ...
ccf-multi-theme --project <path> --all-themes
```

## Execution Flow

### Step 1: Load Themes
```
1. Read config.yaml
2. Load content_themes.json
3. If --all-themes: use all themes in content_themes.json
4. If --themes specified: filter to requested themes only
5. Log: "Multi-theme batch: {T} themes x 12 blueprints = {T*12} total pieces"
```

### Step 2: Sequential Theme Execution
```
For theme in themes:
  
  1. Log: "Theme {i+1}/{T}: {theme.name}"
  2. Select theme's Context Premise
  3. Run: ccf-batch for this theme (Story 7.2)
     - This generates 12 blueprints for the theme
     - Each blueprint goes through full pipeline
  4. Capture theme results
  5. Checkpoint theme progress
  6. Log: "Theme {i+1}/{T}: {authorized}/{total} authorized"
```

### Step 3: Generate Multi-Theme Report
```json
{
  "multi_theme_id": "...",
  "project": "Coach Adele / Batch-W07",
  "themes_processed": T,
  "per_theme": [
    {
      "theme_id": "...",
      "theme_name": "...",
      "blueprints_total": 12,
      "blueprints_authorized": 10,
      "blueprints_remediated": 1,
      "blueprints_escalated": 1,
      "duration_s": 5760,
      "token_usage": {...}
    }
  ],
  "totals": {
    "total_content_pieces": 120,
    "total_authorized": 100,
    "total_duration_s": 57600,
    "total_tokens": 18000000,
    "estimated_cost_usd": 254.00
  }
}
```

## Session Isolation
Each theme gets its own execution context. Theme A's content MUST NOT bleed into Theme B's scripts. This is enforced by:
- Loading only the current theme's Context Premise per batch
- Clearing agent context between theme batches
- Separate checkpoint tracking per theme

## I-R-E-V-C Session Protocol

### INGEST
- Load config.yaml + content_themes.json
- Parse theme selection (--all-themes or --themes list)

### REASON
- For each theme: call ccf-batch with theme context
- Track per-theme and aggregate results

### EMIT
- multi_theme_report.json
- All production artifacts for all themes x blueprints

### VALIDATE
- All requested themes processed
- No cross-theme contamination
- multi_theme_report.json totals are accurate

### CHECKPOINT
- Update config.yaml with multi-theme batch status
