---
name: ccf-init
description: Initialize a new CCF client project with folder structure and config
---

# /ccf-init {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **DOCS_BASE:** `ccf-26/Docs/`

**Objective:** Create the complete CCF project folder structure for a new client and generate the initial `config.yaml`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "pending" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "pending" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "pending" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Ask operator to confirm `{client_name}` identifier (no spaces, lowercase with hyphens)
2. Verify raw input materials are available:

| Check | Description | If Missing |
|-------|-------------|------------|
| 1 | Coach transcripts (≥20,000 words recommended) | WARN → Can proceed but soul extraction will be thin |
| 2 | Business materials (website URL, social profiles) | WARN → Can proceed but tribe extraction will be limited |
| 3 | Audience data (Reddit threads, community comments) | WARN → Can proceed but vibe-comments will be generic |

> [!NOTE]
> Unlike CMF which requires a transcript to proceed, CCF can initialize with partial inputs. However, quality degrades proportionally to missing data.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "pending" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

---

## STEP 2: CREATE STRUCTURE

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "in_progress" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

**ACTIONS:**

Create the following folder structure at `ccf-26/Production/{client_name}/`:

```
{client_name}/
├── config.yaml
├── raw/
│   ├── transcripts/          # Coach transcripts
│   ├── business/             # Website content, social profiles
│   └── audience/             # Reddit threads, community comments
├── intelligence_library/     # Centralized library for extracted intelligence
├── intelligence/
│   ├── soul/                 # soul_values.json, voice_blueprint.md
│   ├── tribe/                # tribe_profile.json
│   ├── themes/               # content_themes.json
│   ├── context_premises/     # {theme}_context_premise_spr.md
│   └── research/             # deep and fresh research briefs
├── output/
│   ├── batches/
│   │   └── batch_001/
│   │       ├── blueprints/   # content_blueprints.json
│   │       ├── soc/          # SoC outputs per blueprint
│   │       ├── adapted/      # Mirror Session outputs
│   │       ├── wisdom/       # Wisdom Forge outputs
│   │       ├── scripts/      # Generated scripts
│   │       ├── analysis/     # Analysis reports
│   │       └── validation/   # AUTHORIZED.md or REJECTION.md
│   ├── logs/                 # error and execution logs
│   └── learning/             # improvement notes, patterns
├── research/
│   ├── fresh/                # {topic}_fresh_brief.md
│   ├── deep/                 # {topic}_deep_brief.md
│   └── vibe_comments/        # vibe_comments_processed.json
└── SETUP_COMPLETE.md         # Created after ccf-theme-discover
```

**Create all directories using `mkdir -p` or equivalent.**

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "completed" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

---

## STEP 3: GENERATE CONFIG

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "completed" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "in_progress" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

**CREATE FILE:** `ccf-26/Production/{client_name}/config.yaml`

```yaml
# CCF Client Configuration
# Generated by ccf-init on {date}

client:
  name: "{client_name}"
  display_name: "{Client Display Name}"
  created: "{ISO date}"

paths:
  base: "ccf-26/Production/{client_name}"
  raw_transcripts: "raw/transcripts/"
  raw_business: "raw/business/"
  raw_audience: "raw/audience/"
  intelligence_library: "intelligence_library/"
  intelligence_soul: "intelligence/soul/"
  intelligence_tribe: "intelligence/tribe/"
  intelligence_themes: "intelligence/themes/"
  intelligence_research: "intelligence/research/"
  output_batches: "output/batches/"
  output_logs: "output/logs/"
  output_learning: "output/learning/"
  research_fresh: "research/fresh/"
  research_deep: "research/deep/"
  research_vibe: "research/vibe_comments/"

skills:
  base: "ccf-26/skills/ccf"
  mfq2_profiler: "setup/emotional-dna-extraction/SKILL.md"
  soul_extraction: "setup/client-soul-extraction/SKILL.md"
  tribe_extraction: "setup/tribe-soul-extraction/SKILL.md"
  theme_discovery: "setup/theme-discovery/SKILL.md"
  soc_generator: "production/soc-generator/SKILL.md"
  mirror_session: "production/mirror-session/SKILL.md"
  wisdom_forge: "production/wisdom-forge/SKILL.md"
  script_generator: "production/script-generator/SKILL.md"
  vibe_comments: "research/vibe-comments/SKILL.md"
  blueprint_orchestrator: "research/blueprint-orchestrator/SKILL.md"
  script_analyst: "validation/script-analyst/SKILL.md"
  script_commander: "validation/script-commander/SKILL.md"
  phoenix_loop: "validation/phoenix-loop/SKILL.md"

models:
  creative: "gemini-2.5-pro"     # SoC, Mirror Session, Wisdom Forge, Scripts
  validation: "gemini-2.5-flash" # Analyst, Commander, Alchemy Gate
  research: "gemini-2.5-pro"     # Deep/Fresh research

temperature:
  voice_priming: 0.9      # SoC Generator
  structured_reasoning: 0.7 # Mirror Session
  dimensional_thinking: 0.8 # Wisdom Forge
  script_execution: 0.3   # Script Generator
  validation: 0.1          # All validators
  research: 0.5            # Deep/Fresh research

sessions:
  setup:
    init: { status: "complete", timestamp: "{ISO date}" }
    mfq2_profile: { status: "pending" }
    soul_extract: { status: "pending" }
    tribe_extract: { status: "pending" }
    theme_discover: { status: "pending" }
  setup_complete: false
  current_batch: null

batch_settings:
  themes_per_batch: 12
  archetypes_per_theme: 3
  scripts_per_batch: 36     # 12 × 3
  max_context_tokens: 100000

validation:
  soul_threshold: 7.0
  protocol_threshold: 8.0
  mimicry_threshold: 7.5
  composite_formula: "(soul * 0.35) + (protocol * 0.30) + (mimicry * 0.35)"
  alchemy_gate: "pass/fail"  # Binary, no partial credit
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "completed" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "pending" }
  ]
});
```

---

## STEP 4: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "completed" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "in_progress" }
  ]
});
```

**CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | config.yaml exists | Valid YAML, all paths populated | ✅/❌ |
| 2 | Folder structure complete | All directories created | ✅/❌ |
| 3 | Raw inputs present | At least transcripts available | ✅/❌ |

**OUTPUT (25-35 words):**
```
✅ CCF PROJECT INITIALIZED
- Client: {client_name}
- Config: config.yaml created
- Structure: All- [x] Folders matched to map
- [x] Config generated
- [x] Next step identified: `/ccf-mfq2-profile {client_name}`
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify raw inputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: CREATE STRUCTURE - Build folder tree", status: "completed" },
    { id: "step-3", description: "STEP 3: GENERATE CONFIG - Create config.yaml", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm structure completeness", status: "completed" }
  ]
});
```

---

## 🔗 NEXT: `/ccf-soul-extract {client_name}`
