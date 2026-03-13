# Prompt-to-Framework Coverage Matrix

**Step 5 Audit — Phase 11**

---

## 1. Consolidation Candidates (Multiple prompts → same archetype)

| archetype_id | Current Prompts | Strategy |
|:-------------|:---------------|:---------|
| `arch_storytelling` (generic) | 10: Anticipation, Connection, Curiosity, Cuteness, Discovery, Empowerment, Joy, Longing, Nostalgia, Recognition, Romance | **→ 1 SKILL.md** with emotion parameter from seed |
| `arch_listicle` (generic) | 6: Curiosity-Intriguing, Hope, Outrageous + 4 Tier Lists + Top Reliable | **→ 2 SKILLs** (listicle + tier list) |
| `arch_debunking_myth` | 3: Disgusting, Fear-Anxiety, Schadenfreude | **→ 1 SKILL.md** with angle parameter |
| `arch_persuasive_tweet` | 3: Persuasive Tweets, Thought Whisperer, Data-Visualizer | **→ 1 SKILL.md** with mode parameter |
| `arch_poll` | 4: Archetypical, Controversial, Stereotypical, Would You Rather | **→ 1 SKILL.md** with poll_type parameter |
| `arch_conceptual_contrast` | 3: Contrast Script, Worst Case Script, Worst Case Visual | **→ 1 SKILL.md** |
| `arch_case_study` (generic) | 2: Intriguing, Relatable | **→ 1 SKILL.md** with variant parameter |

**Post-consolidation: ~38-42 SKILL.md files** (down from 74)

---

## 2. Orphan Prompts (No cross-map entry)

| Prompt | Recommendation |
|:-------|:---------------|
| 4 Meme Archetypes (Benign Violation, Incongruity, Relief Theory, Superiority) | Keep as format-specific SKILLs — referenced by any framework |
| 3 Reaction Archetypes (Nostalgia, Outrage, Validation) | Keep as format-specific SKILLs |
| Hero Journey Visual (×2 — duplicate?) | Audit, remove one if identical |
| Spare Persuasion Priming Activation | Likely obsolete — review against 3-layer priming |

---

## 3. Framework Coverage Gaps

| Framework | `framework_id` | Gap |
|:----------|:-------------|:----|
| Relevance & Timeliness | `fw_01` | No dedicated prompt |
| Combinations | `fw_05` | **Zero coverage** |
| Descriptive/Explanatory | `fw_08` | Caption only (utility) |
| Would You Rather | `fw_10` | Generic poll only |
| Controversial & Comparative | `fw_13` | Partially via polls |
| Controversial & Surprising | `fw_17` | No dedicated prompt |
| Instructional/Advisory | `fw_20` | Caption only (utility) |

**7 of 22 frameworks lack dedicated Script Prompt coverage.**

---

## 4. Unique Prompts That Stay As-Is

| Prompt | archetype_id |
|:-------|:-------------|
| Achievement Story | `arch_achievement_story` |
| Transformation Story | `arch_transformation_story` |
| Inspiration Story | `arch_inspiration_story` |
| Relief Story | `arch_relief_story` |
| Surprise Story | `arch_surprise_story` |
| Shocking Listicle | `arch_shocking_listicle` |
| Funny Relatable Listicle | `arch_funny_relatable_listicle` |
| Nostalgia Listicle | `arch_nostalgia_listicle` |
| Fear-Anxiety Listicle | `arch_fear_anxiety_listicle` |
| FOMO Case Study | `arch_fomo_case_study` |
| Inspirational Case Study | `arch_inspirational_case_study` |
| Social Proof Case Study | `arch_social_proof_case_study` |
| Surprising Case Study | `arch_surprising_case_study` |
| Funny Comparison | `arch_funny_comparison` |
| Outrageous Comparison | `arch_outrageous_comparison` |
| Shocking Comparison | `arch_shocking_comparison` |
| Surprising Comparison | `arch_surprising_comparison` |
| Curiosity Myth | `arch_curiosity_myth` |
| Empowering Myth | `arch_empowering_myth` |
| Indignation Myth | `arch_indignation_myth` |
| Dopamine Cliff Carousel | `arch_dopamine_cliff` |
| Relief Peak Carousel | `arch_relief_peak` |
| Observational Humor | `arch_observational_humor` |
| Visual Timeline | `arch_visual_timeline` |
| SoC Agent | utility — no archetype |
| Content Hook | utility — no archetype |

**~26 prompts map 1:1 to unique archetypes (no consolidation needed).**
