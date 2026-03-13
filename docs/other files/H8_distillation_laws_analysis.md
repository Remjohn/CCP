# First-Principles Analysis: What H8 Is Missing

## How H8 Differs From H10

H10 addresses the **belief layer** — the coach's philosophy, stories, and worldview. H8 addresses the **voice layer** — the coach's vocabulary, metaphors, emotional temperature, and linguistic DNA. Both map to the same `client-soul-extraction/SKILL.md` skill but target different output fields.

**H8 owns:** `emotional_vocabulary[]`, `unique_metaphors[]`, `internal_temperature{}`, `voice_blueprint`, `signature_perspective`
**H10 owns:** `core_values[]`, story inventory, contradictions, evolution tracking

---

## What the Actual Pipeline Does (Voice-Specific Fields)

### From client-soul-extraction/SKILL.md

**C. Unique Metaphors & Language Patterns:**
- Extract metaphors, similes, and analogies the coach uses naturally
- Identify recurring imagery, spatial references, body-based language
- Note transformation vocabulary (before/after, journey, breakthrough)

**D. Signature Emotional Vocabulary:**
- Words and phrases that carry elevated emotional charge
- Expressions used during high-conviction moments
- Verbal intensifiers and qualifiers unique to this speaker
- Minimum: 6+ emotional vocabulary items

**B. Internal Temperature (4-5 sub-topic emotional stances):**
- Maps sub-topics within the content theme to the coach's emotional stance
- Each stance is freeform text describing the coach's position and heat level

**E. Voice Blueprint (exactly 200 words):**
- Synthesis of all extracted elements into a single paragraph
- Must include: pacing, vocabulary level, profanity usage, metaphor density, value integration, speech patterns
- Quality test: "Would someone who knows the coach recognize this voice?"

### From Coach Adele Philosophy Transcript — Voice Evidence

| Voice Feature | What Adele Actually Does | Currently Captured in soul_values.json? |
|:---|:---|:---|
| **Body metaphors** | "like a plant uprooted from soil and put in a pot" / "the body bricolages" / "your blood is de-magnetized" | ✅ Yes — would appear in `unique_metaphors[]` |
| **Code-switching** | French primary, Lingala food terms (matembélé), medical terminology (microbiote, cortisol, porosité intestinale) mixed with street language | ❌ Partially — vocabulary level noted but code-switching pattern not |
| **Direct address** | "don't play with food because you're killing yourselves" / "pray all you want but if you don't take responsibility, poor God has nothing to do with it" | ❌ Partially — profanity level noted but directness register not |
| **Audience interaction vocabulary** | Responds to live questions by reframing them into her framework — "you're asking about postpartum but what you're really asking about is reconnection" | ❌ No — rhetorical patterns not extracted |
| **Temperature shifts** | Goes from calm-explanatory (describing biology) to furious (describing immigration system) to tender (describing her own postpartum) within a single passage | ❌ No — `internal_temperature` is per-topic, not per-emotional-register |

---

## The Gap: 4 Laws vs. H8's Current State

| Component | H0-H5 Pattern (Laws ✅) | H8 Current State ❌ |
|:---|:---|:---|
| **Vocabulary Stratification** | Mode-classified outputs (T/V/R per element) | Flat array — `emotional_vocabulary[]` is a list of words with no context for WHEN the coach uses each word |
| **Metaphor System** | Depth levels (L1/L2/L3) | Flat array — `unique_metaphors[]` lists metaphors but doesn't map them to what they explain or what emotional mode they serve |
| **Temperature Mapping** | Mode × depth classification | Static per-topic — `internal_temperature{}` describes stances but not the RANGE of heat the coach traverses within a topic |
| **Voice as Content Fuel** | Research and stories feed downstream generation | Voice blueprint is a style guide (200 words) — it tells downstream agents HOW to write, but not WHAT vocabulary to deploy in which mode |

---

## What H8 Currently DOESN'T Do (But Should)

### 1. No Vocabulary Stratification

The `emotional_vocabulary[]` array is a flat list:
```json
["combative", "visceral", "mother-fire", "déracinement", "érance médicale"]
```

But Coach Adele uses different vocabularies for different emotional modes:

| Emotional Mode | Vocabulary Register | Example |
|:---|:---|:---|
| **TENSION** (against the system) | Combative, institutional | "migrant", "without legal existence", "errance médicale", "kill your organs" |
| **VULNERABILITY** (her own pain) | Body, intimate | "couldn't carry my child", "lost my memory", "my heart was in the gutter" |
| **RECOGNITION** (validating the tribe) | Communal, ancestral | "honor your body", "your ancestors gave you this", "rituals exist for a reason" |

Without stratification, a downstream SoC generator might use TENSION vocabulary ("kill your organs") in a RECOGNITION scene, producing a tonal mismatch.

### 2. No Metaphor System Mapping

The `unique_metaphors[]` array lists metaphors without mapping them to their function:

```json
["uprooted plant in a pot", "body bricolages", "blood de-magnetized", "black emotion"]
```

But each metaphor in Coach Adele's transcript serves a specific explanatory function:

| Metaphor | Explains | Invoked During | Mode |
|:---|:---|:---|:---|
| "Uprooted plant" | Immigration as biological trauma | TENSION — establishing the structural injustice |
| "Body bricolages" | How the body compensates for climate change | RECOGNITION — validating that the tribe's symptoms are normal adaptation |
| "Blood de-magnetized" | Why anemia is common in Afrodescendant women | VULNERABILITY — connecting self-worth to literal blood chemistry |
| "Black emotion" | Why reactions are explosive | TENSION → RECOGNITION — reframing "anger" as "survival mode" |

Without this mapping, a Blueprint selecting "uprooted plant" for a VULNERABILITY scene doesn't know the metaphor's natural habitat is TENSION.

### 3. No Temperature Range (Only Static Stances)

The `internal_temperature` currently records one temperature per topic:

```json
"immigration_health": "Passionate and combative — believes the system ignores African bodies"
```

But the Coach Adele transcript shows Adele traversing **multiple temperatures within a single topic:**

1. **Start:** Calm, pedagogical (explaining microbiome science)
2. **Middle:** Rising heat (describing what happens when you eat processed food)
3. **Peak:** Furious, direct ("don't play with food — you're killing yourselves")
4. **Drop:** Tender, personal ("I couldn't eat for days, I had 13kg extra")
5. **Resolution:** Empowering, communal ("this is why I created the Yaoui Circle")

This range — from calm explanation to fury to vulnerability to empowerment — IS the coach's voice signature. It's not a static stance; it's a **trajectory**. The current extraction captures only the dominant stance, losing the arc.

### 4. No Voice Blueprint as Content Fuel

The 200-word voice blueprint tells downstream agents style information:
- Pacing: moderate to rapid when passionate
- Vocabulary: mixed medical/colloquial
- Profanity: occasional, targeted

But it doesn't tell them:
- **When to deploy which register:** "Use medical vocabulary when establishing authority (L2 mechanism beats). Use Lingala food terms when building tribal intimacy (RECOGNITION beats). Use direct address when the coach needs to confront the audience (TENSION beats)."
- **What triggers mode switches:** "Adele shifts from pedagogical to combative whenever institutional neglect is mentioned. She shifts from combative to tender whenever her own children are mentioned."
- **What is sacred vocabulary:** Words the coach uses ONLY in specific contexts that should never be deployed casually (e.g., Adele saying "existence juridique" — legal existence — is loaded with 13 years of trauma; it's not a neutral legal term).

---

## The 4 Derived Laws for H8

### Law 1 — Law of Vocabulary Stratification

**Axiom:** "Every word a coach uses carries an emotional charge. A word list without charge context is a dictionary, not a voice."

Every extracted vocabulary item must be tagged with: its emotional mode (T/V/R), the context in which the coach deploys it (when confronting / when revealing / when validating), and its intensity level (standard / elevated / nuclear). Minimum: vocabulary items across all 3 modes.

**Where this integrates:** The `emotional_vocabulary[]` array in `soul_values.json` becomes a structured array with `word`, `mode`, `context`, `intensity` fields.

### Law 2 — Law of Metaphor System

**Axiom:** "A metaphor is not decoration — it's a compression of the coach's entire worldview into a single image. Metaphors without mapping are ornaments."

Every extracted metaphor must be mapped to: what it explains (the concept), which mode it naturally serves (T/V/R), what depth layer it operates at (L1 surface comparison / L2 mechanism explanation / L3 worldview collision), and its source timestamp in the transcript.

**Where this integrates:** The `unique_metaphors[]` array becomes a structured array with `metaphor`, `explains`, `mode`, `depth`, `source_timestamp` fields.

### Law 3 — Law of Temperature Arc (Dynamic Range)

**Axiom:** "A coach's voice is not a static temperature — it's a trajectory. The signature is in the pattern of movement, not the resting state."

For each topic in `internal_temperature`, the extraction must capture not a single stance but a **temperature trajectory**: the starting register, what triggers escalation, the peak, what triggers de-escalation, and the resolution. This trajectory is the coach's emotional fingerprint for that topic.

**Where this integrates:** Each `internal_temperature` entry becomes an object with `start_register`, `escalation_trigger`, `peak`, `de_escalation_trigger`, `resolution` fields.

### Law 4 — Law of Voice Authenticity Gate

**Axiom:** "No generic vocabulary. No borrowed metaphors. Every voice element must be traceable to the coach's own mouth in a specific moment."

Gate checks:
1. **Provenance:** Every vocabulary item and metaphor has a transcript timestamp
2. **Mode coverage:** Voice elements span all 3 modes (T/V/R) — missing mode flags a gap
3. **Temperature range:** Each topic has a dynamic range, not a static stance — flat temperature flags as SHALLOW
4. **Sacred vocabulary:** Words marked as "nuclear" are flagged for downstream agents to handle with care

**Where this integrates:** Added to the I-R-E-V-C `VALIDATE` phase, after schema validation.

---

## Current vs. Law-Governed Comparison

| What Happens Now | What Happens With Laws |
|:---|:---|
| `emotional_vocabulary[]` = flat word list | Vocabulary stratified by mode (T/V/R), context (when), intensity |
| `unique_metaphors[]` = flat metaphor list | Metaphor system mapped: what it explains, mode, depth, source |
| `internal_temperature{}` = one static stance per topic | Temperature arc: start → escalation → peak → de-escalation → resolution |
| `voice_blueprint` = 200-word style guide | Voice blueprint + mode-switch triggers + sacred vocabulary registry |
| No mode classification on voice elements | Every element tagged T/V/R for downstream agent routing |
| No provenance on vocabulary | Every word/metaphor traceable to specific transcript moment |

---

*This analysis grounds the H8 implementation architecture document. The 4 laws (Vocabulary Stratification, Metaphor System, Temperature Arc, Voice Authenticity Gate) are derived from gaps found in the voice-specific output fields of `client-soul-extraction/SKILL.md` and illustrated with real examples from the Coach Adele Philosophy transcript — not from hypothetical use cases.*
