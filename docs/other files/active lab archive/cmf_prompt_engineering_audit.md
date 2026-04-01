# CMF Prompt Engineering Audit
## CCP Doctrine vs. CMF Skill Quality — Should We Rewrite?

**Date**: 2026-03-21  
**Audited Skills**: `witness-hunter` (842 lines), `witness-composer` (539 lines), `story-doctor` (295 lines), `storyboard-composer` (701 lines)  
**Reference Doctrine**: CCF Bible Critique v2 (12 Principles), Script Generation Skill Type Guide v1.0 (8 Mandates)

---

## TL;DR Verdict

**CMF skills do NOT need a full rewrite. They need targeted prompt engineering upgrades.**

The CMF skills are considerably better engineered than the old CCF Bible that the CCP doctrine replaces. Your current skills already avoid several of the Bible's worst mistakes. But the CCP doctrine discovered *new principles* that CMF skills don't implement yet — and these principles would materially improve output quality.

**The ask is not "rewrite 66 skills." The ask is "upgrade 5 specific patterns across 66 skills."**

---

## What CMF Skills Already Do Right

Before listing gaps, credit where it's due. These patterns are **ahead** of the old CCF Bible:

### ✅ 1. Front-Loaded Constraints (Partial)
The `storyboard-composer` mandates PRIMAL + VAE analysis *before* any prompt generation. This aligns with CCP Mandate 3: "Move all quality criteria to the front as pre-generation constraints." The CCF Bible put its quality checks at the *end* as post-hoc self-validation checklists.

### ✅ 2. Anti-Cliché Gates (Visual Skills Only)
The storyboard-composer's `ANTI-CLICHÉ_GATE` in the VAE Decoder and the Banned Visual Elements table are proto-negative-space architecture. They're not as formalized as CCP's 3-level anti-draft, but they exist and work.

### ✅ 3. Verbatim Enforcement
"If it is not in the timecode, it does not exist." This is stronger than anything in the CCP for its domain — the CCP never had to solve the hallucinated-quote problem because it generates content, not extracts it.

### ✅ 4. Structured Output Schemas
Every CMF skill specifies exact JSON/markdown output formats. The CCP doctrine demands this (Block B field_10), and CMF already does it.

### ✅ 5. Validation Gates Are Concrete
The witness-hunter's 8-point checklist (`Coach in HOOK?`, `Proof with Numbers?`) contains *binary, model-executable* checks — exactly what CCP Principle 8 demands. They're not abstract ("Does it sound authentic?").

---

## The 5 Prompt Engineering Gaps

### 🔴 Gap 1: Role-Character Assignments (Principle 7)

**The Problem (CCP Doctrine):** Every time you assign a character role ("You are The Witness Hunter, a specialized agent"), the LLM generates from its prior distribution of what that character produces. Across a 13-step pipeline, the output passes through multiple archetype distributions, producing a committee of archetypes.

**What CMF Does:**
```markdown
# From witness-hunter:
"You are The Witness Hunter, a specialized agent for extracting testimonial scripts."

# From witness-composer:
"I am the Witness Composer. I take the raw quote candidates..."

# From story-doctor:
"You are The Story Doctor, the FIRST AGENT to touch any raw transcript."

# From storyboard-composer:
"I am the Storyboard Composer. I translate human transformation into visual poetry."
```

Every CMF skill opens with a character role assignment. The CCP's discovery: character roles produce *performance*, not *construction*. The fix is cognitive state instructions.

**The Fix for CMF:**

```diff
- You are The Witness Hunter, a specialized agent for extracting 
- testimonial scripts.
+ Cognitive State: Forensic extraction under source fidelity constraint.
+ You are reading a transcript. Your operation is extraction, not 
+ generation. Every output word must trace to a source timecode.
+ Construction properties at this state:
+   - Claims require provenance (timecode + speaker tag)
+   - Missing data is reported, never synthesized
+   - Scoring precedes selection — no quote enters output unscored
```

**Impact:** Medium. CMF skills use roles more lightly than the CCF Bible (they don't say "Channel the voice of a seasoned expert"), but eliminating them would tighten output consistency across the 13-step pipeline.

**Effort:** ~15 min per skill × 66 skills = ~16 hours. But you can batch: narrative skills (hunters, analysts, composers, commanders) share the same cognitive state pattern. Visual skills share another. Sonic/motion share a third. Realistically **3-4 canonical patterns** cover all 66 skills.

---

### 🔴 Gap 2: Post-Hoc Validation Still Present (Principle 3)

**The Problem (CCP Doctrine):** When validation criteria appear at the end of a prompt, the model writes *toward passing them* rather than *from them*. Post-hoc checklists become implicit generation targets, not real validation gates. "Quality theater."

**What CMF Does — Mixed:**

The storyboard-composer does it RIGHT — PRIMAL + VAE run *before* generation. But the narrative skills do it wrong:

```markdown
# From witness-hunter (end of Phase 6):
| **Authentic Voice** | Sounds like real person, not scripted | ✅/❌ |

# From witness-composer (end of Step 4):
| **Coach Count** | Coach mentioned ≥2 times (W1 + W5)? |
| **Duration** | Total duration 60-90 seconds? |
```

"Sounds like real person, not scripted" is not model-executable — it's the exact pattern CCP Principle 8 flags as "quality theater." The coach count and duration checks are legitimately binary and model-executable, but they arrive *after* generation.

**The Fix:**
- Convert model-executable gates (coach count, duration, proof metrics) into **pre-generation constraints** that appear *before* the first instruction
- Remove non-executable gates ("Sounds like real person") entirely — they do nothing
- Keep the checklist format only for post-generation *audit reporting*, not as generation guidance

**Effort:** ~30 min per narrative skill × 40 narrative skills = ~20 hours. But if you fix the witness-hunter as a canonical reference, all 12 other hunters just need the same pattern applied.

---

### 🟡 Gap 3: No Negative Space Architecture (Principle 11)

**The Problem (CCP Doctrine):** A prompt that specifies only what to produce is half a prompt. Without explicit negative space, the LLM defaults to the statistical centroid — the "average AI output" for this task type, which passes surface quality checks.

**What CMF Does:**
- Visual skills have anti-cliché gates and banned elements tables (proto-negative-space) ✅
- Narrative skills have **nothing**. No "what this arc should NOT produce." ❌
- The witness-hunter has "EXAMPLES OF BAD STATEMENTS" per cluster — this is close but arrives too late and isn't structural

**The Fix:** Add a **Negative Space Block** to each arc-specific skill (hunters + composers):

```markdown
## ❌ NEGATIVE SPACE — What The Witness Arc Must NOT Produce

### Archetypal Failure Mode (Level 1):
"I worked with Coach X and it changed my life. Before, I was struggling. 
They helped me see things differently. Now I feel so much better. If you're 
going through something similar, I'd really recommend trying this."

### Failure Diagnosis:
- MECHANISM absent: "helped me see things differently" is description, not lever
- PROOF absent: "feel so much better" contains no falsifiable metric
- CLOSE generic: "recommend trying this" constructs no structural parallel
- HOOK absent: no introduction, no coach presence, no context

### Semantic Distance Instruction:
Output must not share vocabulary, structural pattern, or emotional register 
with the negative demonstration above. Maximum distance from the statistical 
mean is the objective.
```

**Impact:** HIGH. This is the single highest-value upgrade from the CCP doctrine. Generic AI testimonial scripts are CMF's most common failure mode.

**Effort:** ~30 min per arc × 13 arcs = ~6.5 hours. Write the witness-arc exemplar first, then adapt for each of the other 12 arcs.

---

### 🟡 Gap 4: No Causal Construction Sequence (Principle 5)

**The Problem (CCP Doctrine):** If arc phases can be reordered without changing the output, they are a form, not a sequence. Each phase must *create the conditions for the next*.

**What CMF Does:**
```markdown
# From witness-hunter (arc structure):
W1: HOOK (0-8s)   → "Introduce the witness, mention the coach"
W2: PROBLEM (8-20s) → "Describe pain BEFORE the transformation"
W3: MECHANISM (20-35s) → "What the coach did differently"
```

These are *descriptions of content* per phase. They don't specify why W1 must precede W2, or what cognitive state the audience must be in at the *end* of each phase to make the next phase land. They're a form, not a causal sequence.

**The Fix:** Add a one-line **cognitive function** per phase:

```diff
  W1: HOOK (0-8s)
- → "Introduce the witness, mention the coach"
+ → Cognitive function: RECOGNITION ACTIVATION. The audience must see themselves
+   in the witness's world BEFORE the problem is named. Without recognition,
+   the problem phase produces sympathy, not empathy.

  W2: PROBLEM (8-20s)
- → "Describe pain BEFORE the transformation"  
+ → Cognitive function: THREAT ACTIVATION. The audience must feel personal
+   relevance to the problem. Without threat activation, the mechanism phase
+   has no urgency — the viewer watches from outside.
```

**Impact:** Medium. This would make the arc structures more instructional and reduce cases where the LLM treats W1-W5 as interchangeable content buckets.

**Effort:** ~20 min per arc × 13 arcs (hunter + composer) = ~9 hours.

---

### 🟢 Gap 5: No Anti-Draft Exemplars for Narrative Skills

**The Problem (CCP Doctrine):** Level 1 Anti-Draft: a *generated* failure example (3-5 sentences of actual bad prose) that creates semantic repulsion. Descriptions of failure produce abstract avoidance; generated examples produce measurable distance.

**What CMF Does:**
- Storyboard composer has anti-cliché examples ("Stock: Woman sad at table, single tear") ✅ (visual)
- Witness-hunter has "EXAMPLES OF BAD STATEMENTS" ✅ (partial — scattered per cluster, not unified)
- Composers, commanders, and analysts have **nothing** ❌

**The Fix:** Same as Gap 3 above — the Negative Space Block includes the generated failure exemplar. Already covered in Gap 3's effort estimate.

---

## Summary: What Gets Rewritten vs. What Gets Patched

| Component | Action | Effort |
|-----------|--------|--------|
| **Witness-Hunter** | Full upgrade as canonical reference skill | 3-4 hours |
| **Storyboard-Composer** | Patch only (already strongest skill) | 1-2 hours |
| **12 other Hunters** | Propagate canonical patterns from witness-hunter | 6-8 hours |
| **13 Composers** | Add negative space + causal construction | 5-6 hours |
| **13 Analysts** | Light patch (cognitive state header only) | 2-3 hours |
| **14 Commanders** | Light patch (cognitive state + front-load gates) | 2-3 hours |
| **Story Doctor** | Patch (cognitive state, causal decision tree) | 1 hour |
| **Visual skills (4)** | Already strong — minor cognitive state patch | 1 hour |
| **Motion skills (10)** | Cognitive state header + anti-cliché propagation | 2-3 hours |
| **Sonic + Narrative + E-Roll** | Cognitive state header | 1-2 hours |
| **TOTAL** | | **~25-35 hours** |

---

## Recommended Approach

### Phase 1: Write Canonical References (~5 hours)
1. Rewrite `witness-hunter` as the canonical narrative skill
2. Rewrite `storyboard-composer` minor patches as the canonical visual skill
3. These become the "Gold Standard" templates

### Phase 2: Propagate Patterns (~15-20 hours)
4. Propagate witness-hunter patterns to 12 other hunters, 13 composers, 14 commanders
5. Propagate storyboard-composer patterns to motion/sonic skills
6. Each propagation is mechanical — same 5 patterns applied to different arc structures

### Phase 3: Validate (~5 hours)
7. Run one full project (`/cmf-full`) through the upgraded skills
8. Compare output quality against a previous project with old skills
9. Document before/after in a quality report

---

## What NOT To Do

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Port the full Block A/B/C template structure | Apply the 5 patterns above within CMF's existing skill format |
| Add DEP IDs and formal dependency registry to skills | Use the simpler `cmf_dependency_manifest.yaml` from the architecture comparison |
| Implement 3-level anti-draft (CCP Levels 1+2+3) | Implement Level 1 only (archetypal anti-draft — CMF has no per-coach × per-mood combinatorics) |
| Add CRAL wiring protocol | CMF's E-Roll research is architecturally different — it serves visual B-roll, not narrative intelligence |
| Add Maturity Lifecycle / Fingerprint Archive now | Flag for Phase 2 (the Project Fingerprint ID from the architecture comparison) |

---

## Final Take

> The CCF Bible Critique v2 and Script Generation Guide are CCP-specific solutions to CCP-specific problems (voice drift across 97-step pipelines, per-coach × per-mood × per-audience combinatorics, long-running persistent coaching relationships).
>
> But they discovered **5 universal prompt engineering principles** that transcend CCP:
> 1. Cognitive state > character role
> 2. Front-loaded constraints > post-hoc checklists
> 3. Negative space is mandatory
> 4. Phases must be causally connected
> 5. Generated failure exemplars > described failure modes
>
> These 5 principles cost ~25-35 hours to apply across CMF's 66 skills. The ROI is high because CMF runs the same pipeline repeatedly — every project benefits from every improvement.
