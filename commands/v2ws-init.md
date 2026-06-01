---
name: v2ws-init
description: "Initialize V2WS webinar workspace with directory structure and configuration"
agent: Alessandro (Webinar Architect)
ccp_layer: Orchestration (L5)
skills_invoked: [v2ws/orchestration/sop]
---

# v2ws-init

> Initialize a new V2WS webinar production workspace.

## Usage
```
/v2ws-init [webinar_topic] [coach_id]
```

## What This Command Does

1. **Create workspace directory:**
   ```
   production/{coach_id}/v2ws/{webinar_id}/
   ├── research/
   ├── structure/
   ├── slides/
   ├── visual/
   ├── meme/
   ├── voice/
   ├── decks/
   └── config.json
   ```

2. **Load coach configuration:**
   - Copy `coach_soul.json` into workspace
   - Copy `tribe_soul.json` into workspace
   - Copy `ttt_matrix.yaml` calibration

3. **Generate config.json:**
   ```json
   {
     "webinar_id": "auto-generated",
     "topic": "[webinar_topic]",
     "coach_id": "[coach_id]",
     "created_at": "timestamp",
     "status": "initialized",
     "pipeline_stage": "init"
   }
   ```

## Next Step
Run `/v2ws-research` to begin the research phase.
