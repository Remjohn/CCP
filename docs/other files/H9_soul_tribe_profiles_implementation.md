# H9: Soul Tribe Profiles — Implementation Architecture

**Hypothesis:** The tribe profiles must evolve from flat persona cards into depth-stratified, mode-mapped intelligence layers that encode the tribe's visual recognition codes, emotional triggers, and in-group language — making them directly actionable by all downstream agents.

**Pipeline Position:** CCF Setup Phase → feeds H1 (Blueprint), H3 (SoC Voice), H12 (Visual Recipes), H13 (Visual Asset Research), all scripts  
**Existing Infrastructure:** `Tribe Soul Extraction Engine` (exists but surface-level — demographics, stated desires, generic pain points)  
**Gap Classification:** HIGH — Exists but shallow, not mode-tagged, no visual codes  
**MCDA Score:** 8.05 / 10 (Rank #4)  
**Dependency:** Receives from H11 (Raw Target Audience Research)

---

## Section 1: The Input Quality Problem

The current Tribe Soul Extraction Engine produces a persona card: "Afrodescendant women, 30-50, living in Europe, interested in holistic health." This tells the content pipeline WHO the audience is but not HOW they experience life, WHAT they recognize visually, or WHICH emotional triggers create genuine connection vs. performative outreach.

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| H11 Raw Audience Research | Must exist — provides L2/L3 pains, tribal language, visual codes | H11 output |
| H10 Philosophy Brief | For alignment — tribe profiles must be coherent with the coach's philosophy | H10 output |
| H8 Soul Values | For voice coherence — tribe language must resonate with the coach's voice | H8 output |
| Content performance data | Optional but highly valuable — which topics/modes got highest tribal response | Analytics |

---

## Section 2: The 4 Laws of Tribe Profile Distillation

### Law 1 — Mode-Mapped Emotional Triggers

The tribe has emotional triggers that map to the three content modes. Each must be explicitly identified:

- **TENSION triggers:** What makes this tribe angry, frustrated, or urgently activated? What injustices do they feel? What systemic problems affect them? What situation makes them say "ENOUGH"?

- **VULNERABILITY triggers:** What makes this tribe drop their guard? What shared experiences create mutual recognition of pain? What stories make them say "I thought I was the only one"?

- **RECOGNITION triggers:** What makes this tribe feel seen? What visual, linguistic, or experiential cues signal "this was made by someone who is one of us"? What specific references make them smile and share?

**Each mode must have ≥ 3 documented triggers** with source references from H11 research. These triggers become the primary routing intelligence for H1 (Blueprint Orchestrator) — when the blueprint selects MODE: RECOGNITION, it consults the tribe profile for the specific recognition triggers.

### Law 2 — Visual Recognition Code Library

This is the tribe's visual language — the objects, scenes, aesthetics, and cultural artifacts they recognize as "insider" vs. "tourist":

- **Insider objects:** Specific food items, clothing, household objects, tools, spaces that the tribe recognizes instantly. Not "African food" (tourist) but "le mafé de maman" (insider).
- **Insider scenes:** Specific settings, arrangements, activities that feel authentic. Not "a woman cooking" (generic) but "a woman cooking in a European kitchen with African ingredients scattered on the counter" (specific to the diaspora experience).
- **Aesthetic preferences:** Color palettes, lighting warmth, styling choices, photography angles that feel "ours" vs. "about us."
- **Rejection triggers:** Visuals that signal outsider perspective — stock photography tropes, stereotypical representation, tourist-lens aesthetics.

**This library directly feeds H12 (Visual Recipe Distillation Laws) and H13 (Visual Asset Research).** Without it, both visual tracks produce technically competent but tribally inauthentic content.

### Law 3 — In-Group Language Integration

From H11's tribal language extraction, the tribe profile must include operational language intelligence:

- **Terms of address:** How the tribe addresses each other (formal/informal, terms of endearment, generational variations).
- **Conversation patterns:** How the tribe discusses sensitive topics (direct/indirect, humor as deflection, cultural references as shorthand).
- **Engagement signals:** What the tribe says when content resonates ("ça c'est vrai," "elle a tout compris," specific emoji patterns, sharing to Stories vs. sending via DM).
- **Disengagement signals:** What the tribe does when content misses ("too corporate," "she doesn't get it," silence)

### Law 4 — Tribe Profile Authenticity Gate

1. **Mode coverage:** All 3 modes (T/V/R) have ≥ 3 documented triggers with source references.
2. **Visual code depth:** ≥ 5 insider objects/scenes, ≥ 3 rejection triggers. Below threshold → the profile cannot serve H12/H13.
3. **Language verification:** In-group vocabulary items from H11 are integrated. The profile speaks the tribe's language, not the marketer's language.
4. **Experiential grounding:** Every trigger and code traces to H11 research provenance. No assumed tribal behaviors.

---

## Section 3: Output Format

```
soul_tribe_profile_v{N}.json

├── metadata { coach, version, date, H11_version_used }
│
├── tribe_identity
│   ├── who_they_are (experiential, not demographic)
│   ├── daily_reality
│   └── defining_tensions (bicultural, generational, economic)
│
├── emotional_triggers
│   ├── TENSION: [{ trigger, context, evidence_source }]
│   ├── VULNERABILITY: [{ trigger, context, evidence_source }]
│   └── RECOGNITION: [{ trigger, context, evidence_source }]
│
├── visual_codes
│   ├── insider_objects: [{ object, context, recognition_level }]
│   ├── insider_scenes: [{ scene_description, emotional_valence }]
│   ├── aesthetic_preferences: { colors, lighting, styling }
│   └── rejection_triggers: [{ visual, why_rejected }]
│
├── tribal_language
│   ├── in_group_vocabulary: [{ term, context, frequency }]
│   ├── terms_of_address: []
│   ├── engagement_signals: []
│   └── disengagement_signals: []
│
└── content_routing_intelligence
    ├── best_modes_by_topic: [{ topic, primary_mode, secondary_mode }]
    └── archetype_affinity: [{ archetype, expected_resonance, reasoning }]
```

---

## Section 4: 5 Micro-Hypothesis Evaluations

**MH1 — Mode Trigger Coverage:** Each mode (T/V/R) has ≥ 3 triggers with source references. Verifiable: count per mode.

**MH2 — Visual Code Depth:** ≥ 5 insider objects/scenes documented, ≥ 3 rejection triggers. Verifiable: count entries in `visual_codes`.

**MH3 — Language Integration:** ≥ 10 in-group vocabulary items carried from H11. Verifiable: cross-reference against H11 output.

**MH4 — Experiential Grounding:** Select 5 tribal insights. Each must trace to an H11 source reference. Verifiable: check provenance links.

**MH5 — Downstream Routing Test:** Feed the tribe profile to H1 Blueprint Orchestrator alongside a content theme. Does the Blueprint select mode and archetype based on tribal triggers rather than defaulting to generic mode selection? Verifiable: compare blueprint output with and without tribe profile.

---

## Validation Receipt

```
H9 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━
Coach:           [name]
Version:         [N]
H11 Version:     [version used]
Date:            [timestamp]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Mode Triggers:        [T:n V:n R:n]  [PASS/FAIL if any < 3]
Law 2 — Visual Codes:         [insider: n | rejection: n]  [PASS/FAIL]
Law 3 — Language Integration:  [n items from H11]  [PASS/FAIL if < 10]
Law 4 — Authenticity Gate:     [4/4 checks]  [PASS/FAIL]

STATUS: [AUTHENTICATED / SHALLOW / FAILED]
```
