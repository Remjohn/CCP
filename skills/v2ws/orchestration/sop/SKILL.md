---
name: "V2WS Standard Operating Procedure"
description: "Master orchestration SOP for the complete V2WS webinar pipeline"
agent: Alessandro (Webinar Architect)
ccp_layer: Orchestration (L5)
pi_extensions: [TeamOrchestrator, SoulResonance]
inputs:
  - Webinar topic brief
  - coach_soul.json
  - tribe_soul.json
outputs:
  - Complete webinar package (.excalidraw deck + scripts + speaker notes)
---

# 📋 V2WS STANDARD OPERATING PROCEDURE

> Full pipeline: `v2ws-init → v2ws-research → v2ws-structure → v2ws-slides → v2ws-close → v2ws-render`

## Pipeline Phases

### Phase 1: Init (`v2ws-init`)
- Create workspace directory structure
- Load coach_soul.json + tribe_soul.json
- Accept topic brief

### Phase 2: Research (`v2ws-research`)
- Run research planning engine
- Execute deep + fresh research in parallel (TeamOrchestrator)
- Compile research pack

### Phase 3: Structure (`v2ws-structure`)
- Alessandro designs full webinar structure
- Assigns modes (T/V/R) per segment
- Generates intro (6 modules) + transition (3 modules)

### Phase 4: Slides (`v2ws-slides`)
- Elene generates slides per module (parallel via TeamOrchestrator)
- Visual Hook Architect designs visual elements
- TTT × Visual Integration maps temperature to design

### Phase 5: Close (`v2ws-close`)
- Generate 6 close modules
- Handle objections (GhostContext for unvoiced concerns)

### Phase 6: Render (`v2ws-render`)
- Benjamin compiles all slides into `.excalidraw`
- Grant resolves all image assets
- Export final deck + speaker notes + scripts

## Quality Gates
1. **Structure Review:** Alessandro validates T→V→R macro-arc
2. **Vibe Pass:** Ketsia validates audience resonance
3. **Voice Check:** TTT alignment ±2 from baseline
4. **Asset Check:** All images resolved, no broken references
