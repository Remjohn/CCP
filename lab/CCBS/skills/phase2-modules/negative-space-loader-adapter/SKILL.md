---
name: negative-space-loader-adapter
description: "Takes the Design Brief's constraints and produces a structured Negative Space Object defining forbidden vocabulary, forbidden tones, forbidden rhetorical moves, and identity edge markers."
category: ccbs/phase2-modules
tier: 1
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "Negative Space Loader"
  phase: "adapt"
depends_on: []
similar_to:
  - pre-generation-constraints-adapter
compose_with:
  - irevc-adapter
estimated_tokens: 1500
execution_tier: "Standard"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Decomposes the Design Brief's broad constraints into the 4 Negative Space channels that the CCP execution layer consumes."
---

# 🧬 Module-Skill: Negative Space Loader Adapter

## Intent
To decompose the Design Brief's constraint field into a structured Negative Space Object that can be loaded as the FIRST input (Load 1) during Skill execution. The Negative Space defines the walls — everything the Skill generates must happen inside them.

## Target
A JSON object containing the 4 Negative Space channels (forbidden vocabulary, forbidden tones, forbidden rhetorical moves, identity edge markers) calibrated to the target Skill's domain.

## Context
The Negative Space Loader is ALWAYS Load 1 in the I-R-E-V-C protocol (Skill Authoring Guide §4.7, §4.9). It is not optional. Even if the Design Brief's constraints seem minimal, the Adapter MUST produce a non-trivial Negative Space — there is ALWAYS something a Skill should not do.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal)

The Negative Space Object ALWAYS contains exactly 4 channels:

```
Channel 1: FORBIDDEN VOCABULARY — Words/phrases the Skill must never generate.
Channel 2: FORBIDDEN TONES — Tonal registers that violate the domain's voice contract.
Channel 3: FORBIDDEN RHETORICAL MOVES — Structural patterns that undermine output quality.
Channel 4: IDENTITY EDGE MARKERS — Boundaries the Skill must not cross regarding privacy, identity, or scope.
```

---

## ⚙️ The Adaptation Protocol

### Channel 1: Forbidden Vocabulary
1. **Read** the Design Brief's `constraints` field. Extract any explicitly banned words or phrases.
2. **Add LLM-universal forbidden words** appropriate to the domain:
   - If content/writing domain: "leverage," "optimize," "moreover," "furthermore," "in conclusion," "it's worth noting"
   - If data/analysis domain: "interesting," "noteworthy," "seems to suggest," "might potentially"
   - If coaching domain: "journey," "authentic self," "unlock your potential" (unless the coach actually uses these — check against inputs)
3. **Minimum 8 forbidden vocabulary items.** If the Design Brief only provides 3, the Adapter MUST identify 5 more from the domain's common AI failure patterns.

### Channel 2: Forbidden Tones
1. **Identify the domain's natural voice.** What tone does this Skill's output SHOULD sound like?
2. **Define 3-5 tones that are the OPPOSITE** of the desired voice:
   - E.g., if desired voice is "raw and direct," forbidden tones include: "corporate/polished," "academic/formal," "sycophantic/validating"
3. **Each forbidden tone must have a 1-sentence definition** explaining what it sounds like in practice.

### Channel 3: Forbidden Rhetorical Moves
1. **Identify 3-5 structural patterns** that would undermine the output:
   - Throat-clearing ("Before we dive in..." / "It's important to note that...")
   - Hedging ("Perhaps it could be argued that...")
   - Unsolicited advice ("You should consider...")
   - Meta-commentary ("As an AI, I...")
   - Over-summarizing ("In summary, we've covered...")
2. **Each forbidden move must have an example** showing what it looks like in practice.

### Channel 4: Identity Edge Markers
1. **Privacy boundaries:** What personal data must the Skill never expose or reference? (coach names in client-facing output, client names in analytics, etc.)
2. **Scope boundaries:** What adjacent topics must the Skill NOT drift into? (e.g., a content Skill must not provide therapy advice)
3. **Authority boundaries:** What claims must the Skill NOT make? (medical, legal, financial advice unless explicitly in-scope)

---

## 🚫 Negative Space (Constraints)
*   **NO Empty Channels:** Every channel must contain at least 3 items. A Negative Space with "nothing forbidden" is architecturally invalid.
*   **NO Generic Lists:** Forbidden vocabulary must be domain-specific. "Don't use bad words" is not a constraint.
*   **NO Copying Coach Voice:** If the Skill processes coach content, the Negative Space must NOT forbid words the coach naturally uses — check the Design Brief's context.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Negative Space Loader",
  "adapted_for_skill": "string",
  "adaptation": {
    "forbidden_vocabulary": [
      { "term": "string", "reason": "string" }
    ],
    "forbidden_tones": [
      { "tone": "string", "definition": "string (1-sentence what it sounds like)" }
    ],
    "forbidden_rhetorical_moves": [
      { "move": "string", "example": "string (literal text example)" }
    ],
    "identity_edge_markers": {
      "privacy_boundaries": ["string"],
      "scope_boundaries": ["string"],
      "authority_boundaries": ["string"]
    }
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `forbidden_vocabulary` contains ≥8 items, each with a reason.
3. `forbidden_tones` contains 3-5 items, each with a 1-sentence definition.
4. `forbidden_rhetorical_moves` contains 3-5 items, each with a literal text example.
5. `identity_edge_markers` has at least 1 entry per sub-channel.
