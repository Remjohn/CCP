---
name: "Single Blueprint Pipeline Runner"
description: "Runs full production pipeline for one blueprint: SoC -> Mirror -> Wisdom -> Generate -> Validate -> Distribute"
session_id: ccf-produce
phase: orchestration
ccp_layer: Orchestration (L5)
pi_extensions: [TeamOrchestrator]
inputs:
  - config.yaml
  - research/content_blueprints.json (specific blueprint)
outputs:
  - All stage outputs for the specified blueprint
  - execution_report.json with pipeline metrics
depends_on: [all stories 4.1-6.2]
---

# ccf-produce — Single Blueprint Pipeline Runner

## Purpose
Run the full CCF production pipeline for ONE blueprint, enabling end-to-end testing and debugging before running a full 12-blueprint batch.

## Usage
```
ccf-produce --project <path> --blueprint <blueprint_id>
```

## Execution Flow

### Stage 1: SoC Generation (Story 4.1)
```
Session: ccf-soc
Input:  content_blueprints.json[blueprint_id] + coach_soul.json + context_premise_spr.md + vibe_comments
Output: scripts/soc/{blueprint_id}_soc_output.json
Action: Execute skills/ccf/production/soc-generator/SKILL.md
```

### Stage 2: Mirror Session (Story 4.2)
```
Session: ccf-adapt
Input:  soc_output.json + base archetype prompt (via archetype_index.yaml) + coach_soul.json + vibe_comments
Output: scripts/adapted/{blueprint_id}_adapted_prompt.md + reasoning_log.md
Action: Execute skills/ccf/production/mirror-session/SKILL.md
```

### Stage 2.5: Wisdom Forge (Story 4.3)
```
Session: ccf-wisdom
Input:  adapted_prompt.md + deep_research.md + fresh_research.md + vibe_comments + coach_soul.json
Output: scripts/wisdom/{blueprint_id}_wisdom_briefs.json (4 briefs)
Action: Execute skills/ccf/production/wisdom-forge/SKILL.md
```

### Stage 3: Script Generation (Story 4.4)
```
Session: ccf-generate
Input:  adapted_prompt.md + wisdom_briefs.json + coach_soul.json
Output: scripts/final/{blueprint_id}_script.md + generation_report.json
Action: Execute skills/ccf/production/script-generator/SKILL.md
```

### Stage 4: Validation — Script Analyst (Story 5.1)
```
Session: ccf-analyze
Input:  final script + soul_values.json + vibe_comments
Output: validation/analysis/{blueprint_id}_analysis_report.json
Action: Execute skills/ccf/validation/script-analyst/SKILL.md
```

### Stage 5: Validation — Script Commander (Story 5.2)
```
Session: ccf-validate
Input:  final script + analysis_report.json
Output: validation/verdicts/{blueprint_id}_AUTHORIZED.md OR _REJECTION.md
Action: Execute skills/ccf/validation/script-commander/SKILL.md
```

### Stage 6: Conditional Branching
```
IF AUTHORIZED:
  -> Run ccf-distribute for this blueprint (Story 6.1 + 6.2)
  -> Smart Mix generates tweets, captions, quote cards
  -> Art Director selects visual recipe -> visual prompts generated

IF REJECTED:
  -> Trigger Phoenix Loop (Story 5.3)
  -> Mode 1: Targeted Fix -> re-validate
  -> Mode 2: Full Regeneration -> re-validate
  -> Mode 3: Human Escalation -> halt this blueprint
```

## Key Design Decisions

1. **Session Isolation:** Each session runs in its own context window (fresh agent invocation). No cross-session state leakage.
2. **Context Management:** `build_context(phase)` loads only what's needed per session (Story 1.3). Token budget enforced.
3. **Checkpoint Per Session:** After each session completes, checkpoint is saved. Any failure resumes from the last successful checkpoint (Story 1.4).
4. **Token Tracking:** Each session logs input/output token counts for cost monitoring.

## I-R-E-V-C Session Protocol

### INGEST
- Load config.yaml
- Load specific blueprint from content_blueprints.json
- Determine resume point (if any) via check_resume()

### REASON
- Execute sessions in order: SoC -> Mirror -> Wisdom -> Generate -> Analyze -> Validate
- After each session: checkpoint, validate output, proceed to next
- After validation: branch to distribution or phoenix loop

### EMIT
- All stage outputs for this blueprint
- execution_report.json:
  ```json
  {
    "blueprint_id": "...",
    "sessions": [
      {"session_id": "ccf-soc", "status": "complete", "duration_s": 45, "tokens_in": 12000, "tokens_out": 2000},
      {"session_id": "ccf-adapt", "status": "complete", "duration_s": 120, "tokens_in": 35000, "tokens_out": 8000},
      ...
    ],
    "validation": {
      "result": "AUTHORIZED",
      "humanity_score": 8.5,
      "alchemy_average": 7.8,
      "turing_test": "5/5",
      "red_flags": 0
    },
    "distribution": {
      "tweets": 3,
      "captions": 3,
      "visual_prompts": 1
    },
    "total_duration_s": 480,
    "total_tokens": 150000
  }
  ```

### VALIDATE
- All sessions completed successfully (or resumed from checkpoint)
- Final script exists and has a validation verdict
- execution_report.json is complete and accurate

### CHECKPOINT
- Update config.yaml per-session status tracking
- Save execution_report.json to project directory
