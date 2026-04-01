# CMF Video Editing Automation: Feasibility Analysis

## The Question
Should we build an automated video editing pipeline integrated with CMF to achieve 8-12 videos/day throughput?

**Answer: Yes — but scope it surgically. Build only what CMF needs, not a general-purpose video editor.**

---

## Why This Is NOT Over-Engineering

### Your Current Bottleneck Is Clear

CMF's pipeline today:

```
Beat Cluster → E-Roll Research → Visual Prompts → [MANUAL GAP] → Final Video
                                                      ↑
                                               THIS IS THE PROBLEM
```

Every skill in CMF generates **structured outputs** — JSON beat clusters, markdown research distillations, numbered visual prompts. But the final assembly (stitching images + voiceover + music + captions + transitions) is done by hand. **That's your 4-hour bottleneck per video.**

### The Math Makes It Obvious

| Metric | Manual | With Automation |
|--------|--------|-----------------|
| Time per 60-sec video | ~4 hours | ~30 min review |
| Videos per 8-hour day | 2 | 8-12 |
| Monthly output (1 person) | ~40 | ~200+ |
| Cost per video editing | $100+ (editor) | ~$0.50 (compute) |

At 8-12 videos/day, manual editing is **physically impossible**. Automation isn't a luxury — it's the only path to that throughput.

---

## What To Build (Scoped for CMF)

### CMF Needs 3 Things, Not a Full Video Editor

Your research documents cover building general-purpose video editors (Hyperedit), animated game promos (Remotion + Claude Code), and instructional video generators (Playwright + MoviePy). **CMF doesn't need any of that.**

CMF makes 60-second testimonial-style videos with a specific, repeatable structure. What you need:

#### 1. **Timeline Assembler** (Remotion)
Takes CMF's existing structured outputs and assembles a pre-render timeline:

```
INPUTS (already exist in CMF):
├── beat_cluster.json         → timing + narrative structure  
├── visual_prompts.md         → shot descriptions per beat
├── generated_images/         → AI-generated visuals (from visual engine)
├── voiceover.mp3             → AI or recorded narration
└── music.mp3                 → generated background track

OUTPUT:
└── remotion_project/         → React composition ready for review + render
```

> [!IMPORTANT]
> Beat clusters already define your timing grid. This means you DON'T need librosa beat detection or Whisper timestamps for shot placement — your structure is pre-defined by the narrative architecture. The beat cluster IS your Edit Decision List.

#### 2. **Audio Engine** (FFmpeg + Demucs)
Three automated audio tasks:
- **Whisper transcription** → word-level timestamps for captions
- **Demucs stem separation** → isolate music stems for smart ducking  
- **Sidechain compression** → auto-duck music under voiceover

#### 3. **Caption Renderer** (Remotion @remotion/captions)
- Ingests Whisper JSON
- Renders word-by-word animated captions matching CMF's brand style
- Frame-accurate sync comes free from Whisper timestamps

### What NOT To Build

| Feature | Status | Why Skip |
|---------|--------|----------|
| Smart 9:16 cropping | Skip | CMF generates visuals at target aspect ratio already |
| B-roll semantic matching | Skip | CMF's visual prompts already specify exact imagery per beat |
| VLM scene analysis | Skip | No raw footage to analyze — all visuals are AI-generated |
| Agent memory/preferences | Skip | CMF already has `tribe_soul` and `strategy_brief` for style consistency |
| Multiple AI agents (Director/Picasso/DiCaprio) | Skip | Over-engineered for a 60-sec formulaic structure |
| Storyboarding research | Skip | Beat clusters ARE your storyboard |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────┐
│           CMF EXISTING PIPELINE                  │
│  Beat Cluster → E-Roll → Visual Prompts → Images │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│         NEW: VIDEO ASSEMBLY PIPELINE             │
│                                                  │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │ Audio Engine  │    │ Timeline Assembler    │   │
│  │              │    │                      │   │
│  │ • Whisper STT │    │ • Parse beat_cluster │   │
│  │ • Demucs stems│───▶│ • Map images to beats│   │
│  │ • Auto-duck   │    │ • Insert transitions │   │
│  └──────────────┘    │ • Place captions     │   │
│                      │ • Add music + VO     │   │
│                      └──────────┬───────────┘   │
│                                 │               │
│                                 ▼               │
│                      ┌──────────────────┐       │
│                      │ Remotion Preview  │       │
│                      │ (Browser review)  │       │
│                      └────────┬─────────┘       │
│                               │                 │
│                               ▼                 │
│                      ┌──────────────────┐       │
│                      │ Final Render      │       │
│                      │ (1080p MP4)       │       │
│                      └──────────────────┘       │
└─────────────────────────────────────────────────┘
```

### Why Remotion (Not MoviePy or Raw FFmpeg)

| Factor | Remotion | MoviePy | Raw FFmpeg |
|--------|----------|---------|------------|
| AI-manifest-driven | ✅ JSON → React tree | Partial | ❌ |
| Browser preview | ✅ Built-in timeline | ❌ | ❌ |
| Captions integration | ✅ @remotion/captions | Manual | ASS/SRT only |
| Transition library | ✅ @remotion/transitions | Basic crossfades | xfade filter |
| Agent can write code | ✅ React/TypeScript | Python scripts | Filter graphs |
| 9:16 native | ✅ Composition dims | Manual resize | Manual crop |

Remotion wins because **the pre-render timeline is a data artifact, not a creative one.** CMF's beat clusters are already structured data. Remotion converts that data into deterministic video.

---

## Build Phases

### Phase 1: Proof of Concept (1-2 days)
- Install Remotion (`npx create-video@latest`)
- Hand-build ONE 60-second CMF video in Remotion from existing outputs
- Validate: can the beat cluster structure drive Remotion's `<Sequence>` components?
- **Decision gate:** If the mapping works cleanly, proceed. If it doesn't, stop.

### Phase 2: Assembly Skill (3-5 days)
- Create `skills/cmf/assembly/video-assembler/SKILL.md`
- Skill takes CMF outputs → generates Remotion project JSON
- Integrate Whisper for caption timestamps
- Integrate FFmpeg sidechain compression for auto-ducking
- **Output:** A single agent skill that produces a renderable Remotion project

### Phase 3: Style Templates (2-3 days)
- Define 2-3 Remotion templates matching CMF's visual style
- Transition library (preference JSON: which transitions for which arc types)
- Caption styling (font, color, animation pattern per brand)
- LUT color grading preset

### Phase 4: Pipeline Integration (1-2 days)  
- Wire the assembly skill into CMF's commander flow
- Commander triggers assembly after visual engine completes
- Preview → human review → final render loop

**Total estimated effort: 7-12 days for a working pipeline**

---

## What Changes In Your Daily Workflow

### Before (Current)
1. Run CMF pipeline → get visual prompts + images (**automated, ~20 min**)  
2. Open video editor → manually arrange images on timeline (**manual, ~2 hours**)
3. Add voiceover, sync to visuals (**manual, ~45 min**)
4. Add music, duck under VO (**manual, ~30 min**)
5. Add captions (**manual, ~30 min**)
6. Review and export (**manual, ~15 min**)

**Total: ~4 hours per video = 2 videos/day**

### After (With Automation)
1. Run CMF pipeline → get visual prompts + images (**automated, ~20 min**)
2. Assembly skill generates Remotion project (**automated, ~2 min**)
3. Open browser preview → review and adjust (**human, ~15-30 min**)
4. Render final video (**automated, ~2 min**)

**Total: ~40 min per video = 8-12 videos/day**

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Remotion learning curve | Medium | Remotion's Claude Code skill drastically reduces this — agents write the React code, not you |
| Transition quality "uncanny" | Medium | Start with simple crossfades; add sophisticated transitions iteratively |
| Caption sync drift | Low | Whisper + forced alignment gives ±15ms accuracy — well within tolerance |
| Music ducking too aggressive | Low | FFmpeg sidechain params are tunable; save preferences in brand config |
| Scope creep into general editor | High | **Strict scope: CMF assembly only.** Resist building Hyperedit. |

> [!CAUTION]
> The biggest risk is **scope creep**. Your research documents describe building a full Hyperedit SaaS, a game promo pipeline, a storyboarding research system, etc. CMF needs NONE of that. Build the assembler, not the editor.

---

## Verdict

**Build it.** But build THIS:

1. A **Remotion-based assembly skill** that reads CMF's beat cluster JSON and generates a video project
2. An **audio engine** (Whisper + Demucs + FFmpeg) for captions and ducking  
3. A **browser preview** workflow for 15-30 min human review

Don't build: a full video editor, AI B-roll matching, storyboarding agents, multi-agent orchestration, or any of the general-purpose infrastructure described in the research documents.

**The beat cluster is your Edit Decision List. Remotion is your render engine. The gap is just the bridge between them.**
