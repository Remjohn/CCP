# CMF Constraint Network Design
## Zebra-Puzzle Self-Correction Protocol for E-Roll & Visual Engine

**Date:** 2026-03-21
**Derived From:** CCP 33-Point Architectural Stress Test
**Target Skills:** E-Roll Pipeline (4 agents) + Visual Engine (1 agent)

---

## The Core Insight: Why Policy Fails, Why Puzzles Work

From the CCP stress test executive summary:

> *"Policy is obsolete; an instruction to an LLM to 'avoid doing X' will invariably fail at scale due to the statistical phenomenon of mean-reversion."*

**The pattern in the 33 questions is not "check your work." It's this:**

1. **Name a concrete tension** — two valid constraints that conflict
2. **Scenario the failure** — describe exactly what goes wrong if the tension isn't resolved
3. **Force the model to discover the gate** — the model must *derive* the resolution, not recall a rule
4. **Prove downstream awareness** — the answer must acknowledge what the resolution creates or breaks elsewhere

This is structurally identical to a Zebra Puzzle: "The Norwegian lives next to the blue house. The blue house owner drinks water. **What must be true about the green house?**" The model cannot answer without holding the full constraint graph in working memory.

### Policy vs. Constraint — The Failure Anatomy

```
POLICY INSTRUCTION (fails at scale):
  "Make sure your query targets insider-level cultural imagery, 
   not tourist-level stock."

WHY IT FAILS:
  The LLM evaluates "insider-level" against its training distribution.
  Its statistical centroid for "African cultural imagery" IS tourist-level.
  The policy instruction asks it to deviate from its prior, which it does
  for ~3 queries before mean-reverting.

CONSTRAINT PUZZLE (scales):
  "Your finding is 'Kinkeliba tea ritual.' The narrator's sentence at 
   this timestamp is 'Et puis j'ai compris que je méritais mieux.'
   Does Kinkeliba tea PROVE this specific sentence, or does it 
   illustrate the culture AROUND the sentence? If the latter, 
   which of the 4 Laws does it violate?"

WHY IT WORKS:
  The model must hold TWO concrete objects (the finding + the quote)
  and evaluate a LOGICAL RELATIONSHIP between them. It cannot 
  mean-revert because the answer is deterministic — the quote is 
  about self-worth, not about tea. The constraint forces discovery.
```

---

## Design Pattern: The CMF Constraint Question Anatomy

Every constraint question follows this 4-part structure, adapted from the CCP 33-point test:

```
┌─────────────────────────────────────────────────────┐
│  PART 1: THE TENSION (2 valid rules that conflict)  │
│  "X must be true. Y must also be true. X and Y      │
│   cannot both be true simultaneously because..."    │
├─────────────────────────────────────────────────────┤
│  PART 2: THE SCENARIO (what breaks if unresolved)   │
│  "If the agent proceeds without resolving this,     │
│   the output will exhibit [specific failure mode]"  │
├─────────────────────────────────────────────────────┤
│  PART 3: THE RESOLUTION DEMAND (force discovery)    │
│  "Which constraint takes priority? Name the rule,   │
│   cite the source, and state what you will DO."     │
├─────────────────────────────────────────────────────┤
│  PART 4: THE DOWNSTREAM PROOF (systemic awareness)  │  
│  "How does your resolution affect the NEXT agent    │
│   in the pipeline? What must they now account for?" │
└─────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Part 4 is what makes this a NETWORK, not a checklist.** Each question's resolution creates a constraint that feeds into another question. The agent cannot answer Q3 without having resolved Q1. This is the Zebra Puzzle mechanic.

---

# NETWORK A: E-ROLL CONSTRAINT NETWORK

## Placement in Pipeline

```
cultural-introspector → [CONSTRAINT GATE A] → deep-researcher → 
query-generator → [CONSTRAINT GATE B] → research-distiller
```

**Gate A** runs AFTER introspection, BEFORE research begins.
**Gate B** runs AFTER query generation, BEFORE distillation audit.

The gates don't replace the existing 4 Laws — they force the agent to **pre-resolve tensions** that the Laws would otherwise catch too late (after tokens are spent).

---

## GATE A: Pre-Research Constraint Network (7 Questions)

> **Placement:** Inside `deep-researcher-{arc}` SKILL.md, BEFORE Phase 3 (Browser Research).
> **Trigger:** After loading all inputs (tribe_soul, strategy_brief, premise_analysis, beat_cluster) but BEFORE any `web_search` call.
> **Rule:** If any question reveals an unresolved contradiction, the agent MUST reclassify or flag the finding BEFORE searching. Searching with an unresolved tension produces tourist-level results.

### BLOCK 1 — Evidence vs. Illustration (Law 1 × Law 3 Tension)

**CQ-A1. The narrator's quote at beat [{BEAT}] says: "[exact quote from premise_analysis]". Your intended research target from the Cultural Introspection is: "[finding from Q1-Q12 answers]". If you muted the video and showed ONLY an image of your research target, would a viewer understand the narrator's SPECIFIC CLAIM — not the general topic, the CLAIM? State your answer as EVIDENCE or ILLUSTRATION, and if ILLUSTRATION, name which of the 4 Laws this violates and what you will search for instead.**

```
TENSION: Law 1 (Narrative Saturation) says the finding must be culturally 
         deep. Law 3 (Visual Compression) says it must prove a specific 
         narrator sentence. A finding can be culturally deep but narratively 
         disconnected from the specific quote at that timestamp.

SCENARIO: The agent searches for "Kinkeliba tea ritual" at a beat where 
          the narrator says "I realized I deserved better." The result 
          is culturally authentic (Law 1 ✅) but doesn't prove the 
          sentence (Law 3 ❌). Downstream: storyboard-composer receives 
          B-roll that decorates rather than evidences.

RESOLUTION: The agent must state whether the finding PROVES or 
            ILLUSTRATES the specific sentence. If ILLUSTRATION, the 
            agent must either remap the finding to a beat where it IS 
            evidence, or replace it.

DOWNSTREAM: If remapped, the query-generator must know the finding 
            moved beats. If replaced, the new target must be logged 
            for the distiller.
```

**CQ-A2. You have classified your finding for [{BEAT}] as semiotic mode [{T/R/V}]. The beat_cluster.json declares this beat's emotional register as [{register}]. The VCP for this beat reads: "[visual_cinematic_premise]". Does your mode classification match the VCP's emotional texture, or did you assign mode based on the TOPIC rather than the FEELING? If topic-based, reclassify now and state the corrected mode.**

```
TENSION: Law 2 (Semiotic Mode) says mode must match beat register.
         But mode is often assigned based on what the finding IS 
         (a kitchen = RECOGNITION) rather than what the beat FEELS 
         (desperation = TENSION). A kitchen scene during a crisis 
         beat should be TENSION, not RECOGNITION.

SCENARIO: W2 (PROBLEM) has a finding tagged "domestic kitchen hands" 
          (mode: R). But the beat register is TENSION. The query 
          generator builds a RECOGNITION-mode query for a TENSION beat. 
          Downstream: the storyboard-composer receives warm, intimate 
          imagery for a scene that needs harsh, documentary evidence.

RESOLUTION: The agent must evaluate mode against the VCP's emotional 
            texture, not the finding's surface category. If mismatch, 
            reclassify and state the new mode anchor for the query.
```

### BLOCK 2 — Cultural Depth vs. Divisive Heritage

**CQ-A3. Your Cultural Introspection Q7 named [{hero_figure}] as a figure this tribe reveres. Before you search for their imagery, answer: Is this figure universally revered across ALL segments of the tribe, or is there a faction that considers them controversial? If yes, name the controversy. If you cannot name a controversy, state: "I have no evidence of division" — but know that the distiller will flag this if contradicted by the Deep Research.**

```
TENSION: The Introspection requires NAMED figures (not archetypes).
         But tribes are not monolithic — a hero for one segment may 
         be controversial for another. Using their imagery in B-roll 
         silently excludes part of the audience.

SCENARIO: The agent names a political leader as a shared hero. 
          The deep research finds articles showing this figure is 
          polarizing within the diaspora. But the research target 
          was already set, so the search returns laudatory imagery 
          that alienates half the tribe. The video underperforms.

RESOLUTION: The agent must either provide evidence of controversy 
            (triggering a reclassification from "hero" to "divisive") 
            or explicitly stake the claim "universally revered."

DOWNSTREAM: If "divisive," the query-generator must add a filter. 
            If "universally revered" but the distiller later finds 
            contradicting evidence, the CLAIM is traceable.
```

**CQ-A4. Your Cultural Introspection Q4 identified [{sacred_symbol}] as carrying deep meaning. Your Cultural Introspection Q9 identified [{oppressive_system}] as a force that threatened this culture. Does the oppressive system ALSO use or co-opt the sacred symbol? If yes, your B-roll of the symbol will carry unintended connotations. State how you will visually distinguish the tribe's version from the co-opted version.**

```
TENSION: Q4 (sacred symbols) and Q9 (oppressive systems) are answered 
         independently. But colonialism and cultural erasure often 
         co-opt sacred symbols. Showing the symbol without context 
         risks evoking the oppressor, not the tribe.

SCENARIO: A research target is "traditional textile pattern." 
          But that pattern was mass-produced by colonial factories, 
          and generic search results return the commercial version, 
          not the handmade ancestral version. The B-roll reads as 
          "appropriation footage."

RESOLUTION: Name the distinction. The query must contain qualifiers 
            that target the tribe's version (handmade, specific region, 
            named artisan) and EXCLUDE the co-opted version.
```

### BLOCK 3 — Beat Completeness vs. Source Availability

**CQ-A5. The beat_cluster.json contains [{N}] beats. Your Cultural Introspection produced research targets for [{M}] of those beats. If M < N, which beats have NO culturally-grounded research target? For each gap, state: (a) Is it because the transcript doesn't mention this beat's topic culturally? (b) Is it because the introspection questions didn't cover it? Report the gap honestly — do not invent a finding to fill it.**

```
TENSION: The pipeline demands 24+ findings across ALL beats.
         But some beats may have no natural cultural anchor 
         (e.g., W4 PROOF is about metrics, which are culturally 
         neutral). Forcing a cultural finding creates decoration.

SCENARIO: The agent invents a cultural research target for W4 PROOF 
          because the pipeline demands coverage. The result is a 
          beautiful but irrelevant image. Downstream: the distiller 
          flags it as SUPPLEMENTARY, not LOAD-BEARING.

RESOLUTION: Honestly report the gap. The agent must state whether 
            a beat is "culturally anchored" or "metrics-only." 
            For metrics-only beats, the query-generator should target 
            DATA VISUALIZATION imagery, not cultural B-roll.
```

**CQ-A6. Your research targets for [{BEAT}] include both a NAMED PERSON (from Q7/Q10) and a NAMED OBJECT (from Q5/Q6). If the Deep Research Report returns imagery of BOTH, which takes priority in the storyboard? A person and an object in the same 5-second B-roll clip will compete for viewer attention. State which is the PRIMARY visual anchor for this beat and which is SECONDARY (appears in a different shot or is cropped out).**

```
TENSION: E-Roll research serves the visual pipeline. Each beat 
         gets 3-5 seconds of B-roll. Multiple strong findings for 
         the same beat create a visual attention conflict.

SCENARIO: W3 MECHANISM has both "Kinkeliba tea" (object) and 
          "elder doing ceremony" (person). Both land in the same 
          beat. The storyboard-composer doesn't know which to 
          foreground and defaults to a split composition that 
          weakens both. Manual editing required.

RESOLUTION: Rank findings by evidence weight PER BEAT before 
            searching. Primary finding gets the T2I prompt. 
            Secondary finding becomes backup or cross-beat.

DOWNSTREAM: The query-generator uses this ranking to set priority 
            on search queries. The storyboard-composer receives 
            a clear hierarchy.
```

### BLOCK 4 — The Cascade Lock

**CQ-A7. Review your answers to CQ-A1 through CQ-A6. Did resolving any tension CHANGE a finding's beat assignment, mode classification, or priority ranking? If yes, list ALL changes in a single correction manifest. This manifest becomes an input to the query-generator and the distiller. If no changes occurred, state: "All findings stable after constraint resolution."**

```
TENSION: Individual question resolutions can cascade. Remapping 
         a finding from W3 to W5 (CQ-A1) might create an excess 
         at W5 and a gap at W3 (surfaced by CQ-A5). Reclassifying 
         a mode (CQ-A2) might invalidate a priority ranking (CQ-A6).

SCENARIO: The agent resolves each question independently but doesn't 
          check for cascading effects. W3 loses a finding. W5 gains 
          two. The distiller later catches the imbalance but by then(re-search is needed — more tokens, more time.

RESOLUTION: A final manifest that captures ALL changes from CQ-A1 
            through CQ-A6 in one pass. This is the "solution" to the 
            Zebra Puzzle — the state that satisfies all constraints 
            simultaneously.
```

---

## GATE B: Pre-Distillation Constraint Network (5 Questions)

> **Placement:** Inside `query-generator` SKILL.md, AFTER query construction but BEFORE output.
> **Trigger:** After all 24+ queries are drafted but BEFORE writing `ERoll_Search_Queries.json`.
> **Rule:** If any question reveals a violation, the query MUST be corrected inline. The distiller should NEVER be the first to catch these errors.

### BLOCK 1 — Cross-Law Consistency

**CQ-B1. Select the query with the HIGHEST semiotic distance (FAR/TENSION mode) and the query with the LOWEST semiotic distance (NEAR/RECOGNITION mode) from your batch. Are they assigned to DIFFERENT beats? If both are assigned to the SAME beat, you have a mode conflict. A single beat cannot require both documentary-harsh AND domestic-warm imagery. Which mode does the VCP support? Correct the mismatched query.**

```
TENSION: Law 2 mandates mode-per-query. But if the generator assigns 
         contradictory modes to the same beat, the downstream visual 
         pipeline receives conflicting emotional instructions.

SCENARIO: W2 PROBLEM gets both a "documentary harsh" and a "domestic 
          tactile" query. The storyboard-composer must choose a lighting 
          preset. Blade-Through-Shadows (T) and Soft Lantern (R) are 
          incompatible in the same beat. Manual editing to fix tone.
```

**CQ-B2. For each beat, count your queries. You have [{N}] queries for [{BEAT_X}] and [{M}] queries for [{BEAT_Y}]. If the difference is > 2, explain WHY one beat has substantially more research coverage than another. If the reason is "I found more sources," that is NOT a valid architectural reason — it means your research was uneven. Either add queries to the under-covered beat or demote excess queries to SUPPLEMENTARY.**

```
TENSION: Beat coverage should be roughly balanced (4-6 per beat).
         But research depth varies by cultural richness. Some beats 
         attract 8 queries while others get 2. The distiller will 
         catch this, but correcting after search wastes tokens.
```

### BLOCK 2 — Authenticity Self-Test

**CQ-B3. Select any 3 queries at random from your batch. For EACH, answer: "Would this exact query string return useful results if I replaced the cultural reference with a DIFFERENT culture's equivalent?" If YES, the query is generic — it will return stock that happens to match the tribe. A truly saturated query is NON-TRANSFERABLE. Fix any transferable queries by adding the insider signal that makes them tribe-locked.**

```
TENSION: Law 1 (Saturation) and Law 4 (Authenticity) both demand 
         specificity. But the generator can produce queries that LOOK 
         specific ("Kinkeliba morning ritual") while being structurally 
         generic ("[any herb] morning ritual" returns similar results).

SCENARIO: "Kinkeliba morning ritual domestic kitchen" → replace 
          "Kinkeliba" with "Matcha" → returns equally valid results.
          The query is structurally generic. It will return 
          interchangeable imagery that any niche could use.

RESOLUTION: Add the non-transferable signal. "Kinkeliba morning 
            ritual tasse émail bleue Château Rouge" — the blue 
            enamel cup and the Paris neighborhood make it 
            non-transferable to a Japanese tea ceremony context.
```

**CQ-B4. For each query tagged `evidence_test: PASS`, complete this sentence: "If I showed this image to someone who has NEVER seen the video, they would understand that ___________." If your completion is vaguer than the narrator's specific claim, the image is ILLUSTRATION, not EVIDENCE. Downgrade the evidence_test to FAIL and either refine the query or reclassify the finding.**

```
TENSION: Law 3 (Evidence Test) asks "mute the audio, does the image 
         still prove the claim?" But generators often pass this loosely. 
         "Shows transformation" is not the same as "shows 8kg weight 
         loss in 6 weeks."

SCENARIO: evidence_test says "PASS — proves: transformation" for 
          W4 PROOF. But the specific claim is "my energy went from 
          3 to 8 out of 10." No image can prove an energy rating. 
          The correct classification is ILLUSTRATION with a note that 
          W4 requires data-visualization B-roll, not cultural imagery.
```

### BLOCK 3 — The Final Lock

**CQ-B5. Review your complete query batch. Count: (a) Total queries, (b) queries that passed CQ-B3 (non-transferable), (c) queries that survived CQ-B4 (true evidence). If (c) / (a) < 60%, your batch is decoration-heavy. The distiller WILL reject it. State whether you are proceeding with this ratio or revising.**

```
TENSION: The generator's job is to produce 24+ queries. The 
         temptation is to pad with ILLUSTRATION queries to hit 
         the count. This passes the structural validation but 
         fails the load-bearing ratio in the distiller (62.5%).

RESOLUTION: The agent must calculate the ratio BEFORE submission 
            and make an explicit architectural decision: revise 
            or accept the risk that the distiller will reject.
```

---

# NETWORK B: VISUAL ENGINE CONSTRAINT NETWORK

## Placement in Pipeline

```
premise_analysis.json + beat_cluster.json + Brand Avatar + visual_schema
  → [CONSTRAINT GATE C] → storyboard-composer → prompts/SB/*.txt
```

**Gate C** runs INSIDE the storyboard-composer, AFTER PRIMAL + VAE analysis but BEFORE the 6-Block prompt is written.

---

## GATE C: Pre-Prompt Constraint Network (6 Questions)

> **Placement:** Inside `storyboard-composer` SKILL.md, between VAE Decoder and 6-Block composition.
> **Trigger:** After PRIMAL Analysis + VAE Decoder are complete for a beat, BEFORE writing the T2I prompt.
> **Rule:** Each question must be answered PER BEAT. If any reveals a contradiction, the PRIMAL/VAE must be amended before prompt generation.

### BLOCK 1 — Character Anchor vs. Beat Action

**CQ-C1. The Brand Avatar DNA says: "[specific physical description — resting state]". Your PRIMAL BODY TRUTH for this beat says: "[kinetic action]". Does the kinetic action CONTRADICT the avatar's physical description? Example: Avatar says "shoulders collapsed, weight forward" but the beat action is "chest expanding, shoulders rising." If contradiction: the Brand Avatar describes the PERSON, not the POSE. The beat's emotional state overrides the resting pose. Rewrite Block 0 to preserve the avatar's IDENTITY markers (skin, hair, features, clothing) while replacing the POSTURE with the beat-specific action. State what you kept and what you changed.**

```
TENSION: Block 0 (Character Anchor) must be VERBATIM from the Brand 
         Avatar. But PRIMAL demands a kinetic action that may directly 
         oppose the avatar's described posture. Verbatim copying 
         creates frozen, identical characters across all beats.

SCENARIO: Every beat shows Audrey with "shoulders collapsed, fingers 
          pressing temples" because that's the avatar DNA. The PROOF 
          beat should show triumph, but the character looks defeated. 
          Manual editing to fix pose in 3/5 prompts.

RESOLUTION: IDENTITY markers are invariant (skin texture, hair, 
            facial features, clothing base). POSTURE is variant 
            (changes per beat). The agent must explicitly separate 
            these before writing Block 0.

DOWNSTREAM: Every prompt in the project maintains visual consistency 
            (same person) while allowing emotional range (different 
            states). The GMG Expert later validates character 
            consistency across frames.
```

**CQ-C2. Your VAE ANTI-CLICHÉ_GATE identified "[stock pose]" as the generic version of this scene. Your selected Lighting Preset is [{Preset #N}: "{preset description}"]. Does the preset's mood language SEMANTICALLY OVERLAP with ANY element of the banned stock pose? Example: Anti-cliché bans "walking toward sunrise." Preset #3 (Golden Hour Wrap: "warm amber wrapping around subject") evokes EXACTLY this image. If overlap exists: select a different preset that achieves the same EMOTIONAL TEMPERATURE without the cliché resonance. Name both the rejected and selected presets.**

```
TENSION: The anti-cliché gate defines what NOT to show. The lighting 
         presets define the atmosphere. These are defined independently 
         but can semantically collide. "No sunrise walking" + "Golden 
         Hour Wrap" produces exactly what was banned.

SCENARIO: Prompt bans "walking toward sunrise" in Block 6 negative. 
          But Block 4 says "Golden Hour Wrap, warm amber." The image 
          generator interprets both: amber + figure = sunrise walk. 
          The negative prompt fights the positive prompt. Result is 
          an incoherent image. Manual re-generation needed.

RESOLUTION: The agent must cross-check Block 4 against Block 6 
            BEFORE writing. If semantic overlap, swap the preset 
            to one with the same temperature but different visual 
            language (e.g., Soft Lantern instead of Golden Hour).
```

### BLOCK 2 — Source Authority for Environment

**CQ-C3. Three sources describe the environment for this beat: (a) The transcript mentions location "[X]". (b) The visual_schema.json says "[Y]". (c) Your PRIMAL ENVIRONMENT says "[Z]". If all three agree, proceed. If ANY two conflict, state the conflict and declare which source is AUTHORITATIVE for Block 1 (Environment). The hierarchy is: Transcript > visual_schema > PRIMAL inference. If you used PRIMAL inference over a transcript mention, justify why — "artistic choice" is not sufficient.**

```
TENSION: Environment data comes from 3 independent sources. They 
         often conflict. The transcript says "kitchen," the visual 
         schema says "outdoor garden," and PRIMAL infers "bathroom 
         at 3 AM" from emotional analysis.

SCENARIO: The agent picks the most cinematic option (garden, golden 
          hour) over the transcript's actual location (kitchen, 
          fluorescent light). The resulting prompt generates beautiful 
          but fake imagery. The coach recognizes their client didn't 
          have a garden scene. Manual retake.

RESOLUTION: Explicit source hierarchy. Deviation from hierarchy 
            requires a stated architectural reason (e.g., "transcript 
            location is invisible/unphotographable"), not preference.
```

### BLOCK 3 — Word Count Physics

**CQ-C4. Your current PRIMAL + VAE analysis produced [{N}] words of reasoning. Your 6-Block prompt target is 240-280 words, distributed 28/33/25/14 across Character/Environment/Cinematography/Lighting. Before writing, calculate: Block 0 target = [{X}] words. Block 1 target = [{Y}] words. Block 3 target = [{Z}] words. Block 4 target = [{W}] words. Does your PRIMAL analysis contain enough SPECIFIC detail to fill each block, or will you need to PAD any block with generic language to hit the word count? If padding is required, which block will be padded, and what is the risk of generic language in that block?**

```
TENSION: Word count targets enforce prompt structure. But sometimes 
         the PRIMAL analysis doesn't yield enough specifics for a 
         block (e.g., the transcript never mentions the environment). 
         The agent pads with generic language, which the image 
         generator interprets as "stock."

SCENARIO: PRIMAL ENVIRONMENT is "Her kitchen." That's 2 words. 
          Block 1 target is 55-65 words. The agent invents "warm 
          wooden table, morning light filtering through curtains, 
          potted plant on windowsill" — none of which are in the 
          transcript. The image is beautiful fiction.

RESOLUTION: Identify the specific block gap BEFORE writing. If a 
            block will require >30% invented detail, flag it and 
            pull from the E-Roll Deep Research Report as the fill 
            source (culturally grounded) instead of PRIMAL inference 
            (invented).
```

### BLOCK 4 — Shot Distribution Logic

**CQ-C5. The Shot Distribution Guidance table suggests [{shot_type}] for this beat's narrative role. Your PRIMAL analysis and VCP interpretation suggest [{different_shot}]. If they differ, you MUST state your reasoning. "The VCP suggested it" is not sufficient — state the CINEMATIC FUNCTION your chosen shot serves that the guidance shot does not. Example: "I chose Extreme Macro instead of Medium-Close because the beat's evidence is a PHYSICAL SYMPTOM (dry knuckles), not a FACIAL EXPRESSION. Macro proves the symptom; Medium-Close would show a generic 'sad face.'"**

```
TENSION: The guidance table provides defaults. VCP interpretation 
         allows deviation. But unsupported deviation means the agent 
         picked a shot type arbitrarily. Downstream: the GMG Expert 
         expects consistent shot logic across the project.

RESOLUTION: Deviation requires a cinematic function argument, not 
            preference. The argument must reference the specific 
            visual evidence at this beat.
```

### BLOCK 5 — The Cascade Lock

**CQ-C6. Review your answers to CQ-C1 through CQ-C5 for this beat. List any changes you made: (a) Character Anchor posture changes from CQ-C1, (b) Lighting preset swap from CQ-C2, (c) Environment source override from CQ-C3, (d) Block fill-source change from CQ-C4, (e) Shot type deviation from CQ-C5. Does any change CONFLICT with another? Example: CQ-C1 changes the posture to "chest expanding upward" while CQ-C5 selects "Extreme Macro on hands." These conflict — you can't show chest expansion in an extreme macro of hands. If conflicts exist, resolve NOW and state the final configuration.**

```
TENSION: Individual constraint resolutions can create secondary 
         conflicts. The cascade lock forces a final consistency check.

RESOLUTION: A single configuration state that satisfies all 5 
            constraints simultaneously. This is the "Zebra Puzzle 
            solution" for this beat — the unique configuration where 
            all constraints hold.
```

---

## Implementation: Where Each Gate Goes

### File Modifications

| Gate | Target Skill File | Insert Location |
|------|-------------------|-----------------|
| **Gate A** (7 Qs) | `skills/cmf/eroll/deep-researcher-{arc}/SKILL.md` (×13 arcs) | After "PHASE 1: CONTEXT LOADING", before "PHASE 2: 12 VISUAL RESEARCH QUESTIONS" |
| **Gate B** (5 Qs) | `skills/cmf/eroll/query-generator/SKILL.md` | After "Query Generation Rules", before "Output: Search Queries JSON" |
| **Gate C** (6 Qs) | `skills/cmf/visual/storyboard-composer/SKILL.md` | After "The VAE Decoder Protocol", before "The 7-Block Prompt Structure" |

### Output Format for Constraint Answers

Each gate produces a **Constraint Resolution Manifest** appended to the agent's output:

```json
{
  "constraint_network": "GATE_A",
  "questions_answered": 7,
  "corrections_made": [
    {
      "question": "CQ-A1",
      "beat": "W3",
      "change": "Reclassified 'Kinkeliba tea' from EVIDENCE to ILLUSTRATION",
      "action": "Replaced with 'Coach's specific method name' as evidence target",
      "downstream_impact": "Query generator must use new target for W3"
    }
  ],
  "cascade_conflicts": 0,
  "final_status": "ALL_CONSTRAINTS_RESOLVED"
}
```

The distiller and the storyboard-composer can then CHECK this manifest against their inputs, creating an end-to-end traceability chain.

---

## Verification Plan

### Test 1: Before/After Comparison
1. Run one project through the E-Roll pipeline WITHOUT constraint gates (current behavior)
2. Run the SAME project through WITH constraint gates
3. Count the number of findings the distiller rejects in each run
4. **Success metric:** Distiller rejection rate drops by ≥40%

### Test 2: Manual Editing Reduction
1. Run one project through the full pipeline WITH constraint gates
2. Track manual edits required by the operator after storyboard generation
3. Compare against the average from last 3 projects
4. **Success metric:** Manual edit count drops by ≥50%

### Test 3: Constraint Cascade Integrity
1. Deliberately introduce a contradiction (e.g., RECOGNITION-mode finding on a TENSION beat)
2. Verify Gate A catches it at CQ-A2
3. Verify CQ-A7 reports the cascade change
4. Verify the query-generator receives the corrected mode
5. **Success metric:** Zero contradictions leak past the gate

---

## What This Network Does NOT Replace

| Existing Mechanism | Status | Rationale |
|---|---|---|
| 4 Laws of Visual Search Distillation | **KEPT** | The Laws are the evaluation standard. The constraint network is the pre-generation reasoning that prevents Law violations. |
| Research Distiller (auditor agent) | **KEPT** | The distiller is the final validator. The constraint network reduces distiller rejections, not replaces them. |
| PRIMAL + VAE Protocol | **KEPT** | The constraint network runs AFTER PRIMAL/VAE, forcing cross-check of their outputs. |
| Quality Gates (storyboard-composer) | **KEPT** | The 9 quality gates are post-generation checks. The constraint network is pre-generation reasoning. |

The constraint network is a **reasoning layer**, not a validation layer. It forces the agent to THINK before DOING. The existing validators catch what gets through.
