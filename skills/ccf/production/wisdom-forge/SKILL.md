---
name: "Wisdom Forge - Stage 2.5"
description: "Generates 4 wisdom briefs between adaptation and generation"
session_id: ccf-wisdom
phase: production
stage: 2.5
ccp_layer: Deep Reasoning (L3)
pi_extensions: [MemoryFolder]
inputs:
  - config.yaml
  - scripts/adapted/{blueprint_id}_adapted_prompt.md (from Stage 2)
  - research/deep/{blueprint_id}_deep_research.md
  - research/fresh/{blueprint_id}_fresh_research.md
  - research/vibe_comments_processed.json
  - intelligence/soul/coach_soul.json
outputs:
  - scripts/wisdom/{blueprint_id}_wisdom_briefs.json (4 briefs)
depends_on: [story-4.2, story-3.3, story-3.4, story-3.5]
---

# Stage 2.5: The Wisdom Forge — Brainstorm
## Separating Cognitive Processes: Archetype Intelligence → Dimensional Wisdom → Performance

---

## The Separation Principle

> "Each agent should do ONE type of thinking."

## Critical Rules — The 4 Laws of Wisdom Filtration (H15)

> [!CAUTION]
> **These 4 Laws are hard constraints. They prevent the 4 briefs from converging into the same generic summary.**

### LAW 1: Dimensional Separation (Anti-Convergence)
Each of the 4 wisdom briefs must operate on a fundamentally different axis of truth, producing zero thematic or conceptual overlap.
- **Deep** = Timeless Reframe (Intriguing/Outrageous). 
- **Fresh** = Current Urgency (Alarming/Potential). 
- **Authenticity** = Shared Reality (Satisfying). 
- **Memetic** = Tribal Signal.
If you can swap any two briefs and the script doesn't change → the briefs failed to create dimensional tension.

### LAW 2: Contextual Translation (Anti-Content)
No brief may output raw data, statistics, or general facts without explicitly stating the consequence, causality, or existential meaning of that data for the specific target audience. Facts are disposable; meaning is sticky. Every research finding must answer the "SO WHAT?" question. Not "Inflation is at 4%," but "The wealth you built over the last 10 years is quietly evaporating while you sleep."

### LAW 3: The Shadow (Anti-Perfection)
At least one insight across the 4 briefs must acknowledge a contradiction, a painful truth, a limitation of the coach's doctrine, or a valid counter-argument. Purely positive, motivational content triggers the psychological deception filter. Admitting the shadow builds immediate trust.

### LAW 4: The Information Gap (Anti-Resolution)
The briefs must design specific tension points where information is intentionally withheld or framed as a question. AI is an answer machine; humans engage with question machines. Handing Stage 3 a fully resolved argument results in a boring script. Each brief must provide Stage 3 with the *signal* to open a gap, not the *answer* that closes it.

| Stage | Thinking Type | Lens | Output |
|-------|--------------|------|--------|
| Research Analysts (96) | **ARCHETYPE thinking** | "What does this format need?" | Archetype-biased briefs |
| Stage 1 (SoC) | **VOICE thinking** | "How do I naturally talk about this?" | Coach-voice priming |
| Stage 2 (Mirror Session) | **STRUCTURAL thinking** | "How should the prompt be adapted?" | Adapted prompt framework |
| **Stage 2.5 (Wisdom Forge)** | **DIMENSIONAL thinking** | "What does all this MEAN for my audience?" | 4 wisdom briefs |
| Stage 3 (Performance) | **EXECUTION** | "Perform." | Script |

**The problem with the current pipeline:** Stage 3 has to simultaneously:
1. Follow archetype structural rules
2. Process research into useful insights
3. Apply authenticity filtering on the fly
4. Verify memetic triggers
5. Generate in coach voice

**That's 5 cognitive tasks in one call.** Stage 2.5 peels off #2, #3, and #4 into pre-processed briefs — so Stage 3 only does #1 and #5 (structure + voice = performance).

---

## Alchemy Principles Governing Stage 2.5

These principles from the Conscious Movie Alchemy are the RULES that Stage 2.5 must follow. They're not suggestions — they're structural constraints.

| # | Principle | What It Demands of Stage 2.5 |
|---|-----------|------------------------------|
| 1 | **Vulnerability precedes connection — but the doctrine always wins** | You CAN'T create genuine connection from invulnerability. People don't connect with perfection — they connect with the moments you felt hesitation, fear, or imposter syndrome. **BUT** the vulnerability is in the FEELING, not in the ACTION. The coach ACKNOWLEDGES the feeling ("I felt the same fear you feel") → then shows they TOOK ACTION ANYWAY ("but I followed the doctrine") → and RESULTS PROVE IT ("and it works"). Three-part move: **FELT IT → DID IT ANYWAY → RESULTS.** The feelings are real but they NEVER guide the coach. Data, discipline, and the system guide the coach. You literally can't demonstrate competence without showing both sides — a coach who never felt doubt isn't relatable, a coach who felt doubt and acted anyway IS the proof of mastery. This is a DELIVERY sequence — applies to coach output, NOT to audience input processing. |
| 2 | **Authority comes from being right about what matters** | The Wisdom Briefs shouldn't try to cover everything from the research. They should identify the ONE thing in the coach's domain that determines outcomes — and be RIGHT about it. Curation > coverage. Being right about what matters > appearing certain about everything. |
| 3 | **The Information Gap (Curiosity)** | AI is an "answer machine" — it rushes to solutions. Great storytelling is a "question machine" — it holds back resolution, creating tension. The Wisdom Briefs must identify WHERE TO HOLD BACK. Where is the question more engaging than the answer? We stay for the tension, not the perfection. |
| 4 | **Humans crave context, not content** | Raw research briefs are CONTENT — data, stats, studies. The Wisdom Briefs must transform content into CONTEXT — meaning, consequence, causality, relationships. Not "what the data says" but "what the data MEANS in the larger frame of the audience's life." |
| 5 | **Audience comments are raw signal** | The audience doesn't need to earn permission to be vulnerable. They just ARE. Their comments are unfiltered truth — fears, suspicions, hopes. The competence→vulnerability sequence applies to the COACH's delivery, never to how we read audience reactions. Don't filter audience signal through coach principles. |
| 6 | **The Paradox of Specificity** | "The more specific you are, the more universal the emotion becomes." AI defaults to the average — generalizations that trigger the audience's deception filter. "The system is rigged" = cliché. "The median-income family can no longer afford the median-priced home for the first time in recorded history" = truth recognition. **Truth Recognition without Specificity = Cliché.** The Wisdom Briefs must produce SPECIFIC, granular, sensory-level truths — not universal taglines everyone already heard from ChatGPT. Specificity bypasses the skepticism filter because it's harder to fabricate. |
| 7 | **Story is the vessel, not the decoration** | Facts are disposable; narrative is sticky because it encodes meaning, identity, and values. Vulnerability lives in the STORY. Humans act on stories, not data. |
| 8 | **Tribal Alignment (Status)** | We consume content to signal WHO WE ARE. "Accurate" content pushes some away to pull the *right* tribe closer. Polarization is value. Vibe-baiting means signaling to the tribe, not pleasing the crowd. |
| 9 | **The Shadow (Complexity)** | Humans know life is messy. We crave stories that acknowledge the "Shadow" — the grey, contradictory parts of life. Safe content is ignored; content that admits the hero is flawed or the villain has a point builds trust. |
| 10 | **Accuracy > Perfection** | Emotion is specific. A trembling voice hits harder than flawless acting. Content resonates when it reflects *lived truth*, even if messy. |

> [!CAUTION]
> **The critical distinction:** Principles 1-2 apply to COACH OUTPUT (how the script is delivered). Principle 5 applies to AUDIENCE INPUT (how comments are processed). Principles 6-10 apply to ALL outputs — every truth claim must pass the specificity test, be narratable, align with the tribe, acknowledge the shadow, and prioritize accuracy over perfection. Confusing actors or skipping these gates breaks the system.

---

## What Already Exists in Archetype Prompts (Verified)

Looking at the Authority Tier List archetype as reference:

### Authenticity Protocol (Currently 3 Steps — Stage 3 does this live)

```
Step 1: SOUL AUTHORITY CALIBRATION
- What gives THIS person credibility?
- Their decision-making philosophy
- Their authority temperature (gentle guide vs firm judge)
- Their value hierarchy

Step 2: TRIBAL GUIDANCE LANGUAGE
- What decision paralysis does the tribe experience?
- What language do they use when seeking guidance?
- What false authorities have burned them?
- What tribal values determine "quality"?

Step 3: AUTHENTICITY FILTERING
- Every choice must reflect genuine assessment
- Match their natural confidence level
- Never rank based on mainstream consensus unless coach agrees
- Never try to appear more expert than coach naturally is
```

### Memetic Trigger Protocol (Currently 4 Pillars — Stage 3 verifies after generating)

```
Pillar 1: IMMEDIATE COMPREHENSION
- Can the audience understand this in 3 seconds?

Pillar 2: HIGH-AROUSAL EMOTION
- Primary emotion identified (Relief, Vindication, etc.)
- Surprise + validation moments planned

Pillar 3: TRIBAL SIGNAL
- Rankings reflect tribe quality standards
- Tribe language used
- At least one tribal in-joke per tier 

Pillar 4: INHERENT SHAREABILITY
- Social currency value
- Utility share value
- Conversation starter potential
```

### The Problem

These protocols are currently **INSTRUCTIONS**. Stage 3 reads them, tries to follow them, and generates simultaneously. But:

- The Authenticity Protocol requires **introspection** — deep self-examination
- The Memetic Protocol requires **audience analysis** — dimensional thinking
- Neither is "execution" work — both are **reasoning** work

**Reasoning ≠ performance.** Asking Stage 3 to reason AND perform is like asking a musician to compose AND play at the same time. Possible, but the quality of both suffers.

---

## The 4 Wisdom Briefs

### Brief 1: Deep Wisdom Brief
*Processing: Deep Research Brief → transform content into context*

**Input:** 1,600-1,800 word archetype-processed deep research brief

**Governing principles:** Context not Content (#4), Authority = right about what matters (#2), Information Gap (#3)

**The coach asks themselves (WIP lenses):**

```
CONTEXT: What is the LARGER FRAME that makes this research 
matter to my audience's life? Not data — meaning. Not stats — 
consequence. Not findings — causality. What is the relationship 
between this research and something my audience is LIVING 
right now? (Alchemy: humans crave context, not content)

REVELATION: From this entire brief, what is the ONE thing 
that — if I'm RIGHT about it — determines outcomes in my 
domain? Not the most interesting finding. The one that 
MATTERS. (Alchemy: authority = being right about what matters)

INFORMATION GAP: What does this research OPEN as a question 
that I should NOT immediately answer? Where is the tension? 
What gap between "what they know" and "what they need to know" 
creates the itch that keeps them watching? I am a question 
machine, not an answer machine. (Alchemy: Information Gap)

CURATION: What from this 1,800-word brief should I LEAVE OUT? 
What's expected, generic, or would make my audience's eyes 
glaze over? What disconnected content has no context?

WEAPON: My loaded line — the sentence that delivers this 
context as a punch, not a lecture. (60-70 words)
```

**Output:** ~200 words of coach-processed deep wisdom

---

### Brief 2: Fresh Wisdom Brief
*Processing: Fresh Research Brief → transform current data into urgency + tension*

**Input:** 500-600 word archetype-processed fresh research brief

**Governing principles:** Information Gap (#3), Context not Content (#4), Authority = right about what matters (#2)

**The coach asks themselves:**

```
URGENCY: What from this recent data makes this topic 
matter MORE right now than it did 6 months ago? What shifted? 
What CONTEXT changed? (Not just "new data" — what does the 
new data MEAN for people's lives?)

AMMUNITION: What is the ONE number, stat, or recent event 
that I can drop like a bomb? The "chiffre-choc"? This is 
the fact I need to be RIGHT about — the one that determines 
outcomes. (Alchemy: right about what matters)

COUNTER-NARRATIVE: What current trend or popular opinion 
does this fresh data CONTRADICT? Where is the mainstream 
wrong RIGHT NOW?

GAP DESIGN: What does this fresh data REVEAL that should 
be held back as a question before being answered? What 
opening line creates the itch? The tension that makes them 
stay? (Alchemy: question machine, not answer machine)

WEAPON: The opening line that uses this fresh context to 
stop the scroll. (60-70 words)
```

**Output:** ~200 words of coach-processed fresh wisdom

---

### Brief 3: Authenticity Introspection Brief
*Processing: Coach Soul Values + SoC → structured self-examination*

This is where the Authenticity Protocol stops being instructions and becomes **THINKING**.

**Input:** soul_values.json + SoC output + context_premise

**Governing principles:** Competence precedes vulnerability (#1), Authority = right about what matters (#2)

**The coach asks themselves:**

```
CREDIBILITY (the competence gate): Why should I be the one 
talking about this? Not my resume — my REAL reason. What have 
I lived, witnessed, or learned that gives me the right to speak? 
What am I consistently RIGHT about in my domain that determines 
outcomes? (Alchemy: authority = being right about what matters)

BOUNDARIES: What WON'T I say about this topic? What lines 
do I refuse to cross? What popular opinions do I genuinely 
disagree with? Where does my integrity draw the line?

THE HUMAN UNDERNEATH (vulnerability that builds connection): 
The coach ACKNOWLEDGES the real feelings — the hesitation, 
the procrastination, the imposter syndrome. These are REAL.
But then: "I felt this way AND I took action anyway."
The feelings don't guide me. The doctrine guides me.

The three-part move:
1. I FELT IT (the vulnerability — what creates connection)
   "I felt like staying in bed. I wanted to quit."
2. I DID IT ANYWAY (the discipline — what demonstrates competence)
   "But I followed the system. I don't let feelings drive action."
3. RESULTS PROVE IT (the evidence — what solidifies authority)
   "And here's what happened because I did."

You CAN'T demonstrate competence without showing both sides.
A coach who never felt doubt isn't relatable.
A coach who felt doubt and acted anyway — THAT'S mastery.
(Alchemy: vulnerability precedes connection, but the doctrine 
always wins. You have the system. You follow it.)

VOICE TEMPERATURE: For THIS specific topic with THIS audience, 
what's my natural temperature? Am I angry? Protective? Playful? 
Serious? Where does my gut land?

TRUTH: If I could only say ONE thing about this topic and 
never speak about it again, what would it be? (60-70 words)
```

**Output:** ~200 words of coach self-examination

**Why this matters:** Currently, the LLM does a "Soul Authority Calibration" by READING the soul_values.json and making inferences. But inference ≠ introspection. When the coach (simulated) actually ANSWERS these questions, the output has dramatically more specificity and authenticity than when Stage 3 tries to "match voice patterns" from a JSON file.

**The Trust Equation:** COMPETENCE (Attraction) + VULNERABILITY (Retention) = DEEP CONNECTION.

> [!CAUTION]
> **Vulnerability precedes connection ONLY AFTER trust is built.** You can't lead with vulnerability if there's no trust. But they can't TRUST you if you aren't Competent.
> *   **Competence is the Art of Attracting.** People listen because you know the way.
> *   **Vulnerability is the Art of Retention.** People STAY and REMEMBER because you made them feel seen.
> Information is not as memorable as feelings. They may forget what you said, but never how you made them feel.

| | ❌ Vulnerability that UNDERMINES authority | ✅ Vulnerability that RETAINS the tribe |
|---|---|---|
| The feeling | NOT acknowledged | Acknowledged openly: "I felt it too" |
| The action | Guided by the feeling | Guided by the DOCTRINE despite the feeling |
| The result | Doubt remains | Results prove the system works |
| The dynamic | Repels (shows weakness) | Retains (shows shared humanity + strength) |

**Why you CAN'T skip the vulnerability:** A coach who never felt doubt isn't human. A coach who felt doubt and ACTED ANYWAY is proof that the doctrine works. The vulnerability is the SETUP. The action is the PAYOFF. The results are the PROOF. Without the setup, the payoff means nothing.

---

### Brief 4: Memetic Vibe Signals
*Processing: Community comments + context_premise → audience reaction architecture*

This is where the Memetic Trigger Protocol stops being a checklist and becomes **STRATEGY**.

**Input:** 70 community comments (organized by VRC/VCC dimensions) + context_premise + archetype memetic requirements

**Governing principles:** Audience = raw signal (#5), Information Gap (#3), Context not Content (#4)

> [!IMPORTANT]
> **Audience comments are UNFILTERED SIGNAL.** Don't apply coach principles (competence, authority) to audience data. The audience's vulnerability, confusion, fears, and hopes are the raw material. Their value is in being AUTHENTIC, not competent. Read them for what they ARE, not what they should be.

**The coach asks themselves:**

```
COMPREHENSION SIGNAL: What is the SINGLE clearest way to 
present this topic so my audience gets it in 3 seconds? 
What CONTEXT do they already have that I can plug into? 
Not information — the frame of meaning they already carry. 
(Alchemy: context, not content)

EMOTION ARCHITECTURE: Reading these raw, unfiltered comments 
— what is the PRIMARY emotion the audience is ALREADY feeling? 
What they actually express, not what I think they should feel. 
And what SECONDARY emotion creates depth? Map these to 
specific script moments.

TRIBAL CODE: What language from these comments is TRIBAL? 
What phrases are "our people" signals? What in-group 
references would make outsiders confused but insiders 
feel recognized? What raw audience signal should I MIRROR, 
not filter?

INFORMATION GAP DESIGN: Where should the script CREATE 
tension by holding back? What do these comments reveal the 
audience WANTS to know but doesn't yet? Design the gap 
between what they know and what they need to know. We stay 
for the tension, not the perfection. (Alchemy: Information Gap)

ARCHITECTURE: The comment section blueprint — what should 
the top 3 comments look like? (60-70 words)
```

**Output:** ~200 words of memetic strategy

**This absorbs the AIP comment processing from Phase C AND applies the Memetic Protocol.** Instead of separate steps, the coach processes audience signal THROUGH the memetic pillars — treating comments as raw truth, not filtered data.

---

## Truth Recognition = The Hook Mechanism

**Why Truth Recognition IS the hook:**

The hook's job is to make the audience stay. The audience stays when their brain says "this person sees what I see." That IS truth recognition. The 3-second hook isn't delivering a truth — it's **SIGNALING** that a truth recognition is coming.

This connects directly to the Information Gap: the hook OPENS the gap by signaling "I know something specific about YOUR situation." A cliché hook CLOSES the gap because the audience already knows where it's going.

### The 5 Types of Truth Recognition

Not all truth recognition works the same way. Each type activates a different emotional circuit:

| Type | Brain Response | What It Opens | Hook Pattern |
|------|---------------|---------------|--------------|
| **Potential** | "Could this be true?" | Curiosity gap | "What if every financial plan you've made was designed to fail?" |
| **Intriguing** | "I never saw it that way" | Reframe activation | "The people who budget the hardest stay the poorest" |
| **Outrageous** | "No way… but actually yes" | Shock + validation | "Your bank made $4.2B last quarter from a fee you don't know you're paying" |
| **Alarming** | "This is worse than I thought" | Urgency | "745,000 people died last year from the schedule you're working right now" |
| **Satisfying** | "FINALLY someone said it" | Relief + vindication | "You were right about your 401k — here's the proof your advisor didn't show you" |

### The Shadow Principle

> [!IMPORTANT]
> **Even a SHADOW of a specific truth in any of these categories holds more value than a fully stated cliché.**
>
> A shadow of specific truth **OPENS** the information gap → "wait, tell me more"
> A cliché truth **CLOSES** the gap instantly → "heard it, next"
>
> The audience stays for the tension of an almost-revealed specific truth. They scroll past a fully-revealed generic one.

**Compare:**

| | Cliché (gap closes) | Shadow of Specific Truth (gap opens) |
|---|---|---|
| Same "truth" | "The system is rigged" | "Your bank made $4.2B last quarter from a fee you don't know you're paying" |
| Same "truth" | "Hustle culture is toxic" | "745,000 people died last year from the schedule you're working right now" |
| Same "truth" | "Most financial advice is wrong" | "Your advisor's recommended portfolio has underperformed a basic index for 14 straight years" |

**Both columns point to the same underlying truth.** But the left column is what ChatGPT produces — the statistically most probable output. The right column is what someone who ACTUALLY KNOWS something produces — the specific, granular, sensory detail that can't be fabricated.

### What This Means for the 4 Wisdom Briefs

Each brief's WEAPON line (the 60-70 word output) should be evaluated not just for specificity, but for **which TYPE of truth recognition it deploys**:

| Brief | Best Truth Recognition Type | Why |
|-------|---------------------------|-----|
| **Deep Wisdom** | **Intriguing** or **Outrageous** | Timeless research reframed through coach's lens — the audience should think "I never saw it that way" |
| **Fresh Wisdom** | **Alarming** or **Potential** | Current data creates urgency or opens a curiosity gap about what's coming |
| **Authenticity** | **Satisfying** | The coach validates what the audience already suspects — "finally someone who sees what I see" |
| **Memetic** | Depends on dimension | Each VRC/VCC dimension may map to a different truth recognition type based on the audience's raw signal |

**The brief doesn't need to deliver the complete truth. It needs to deliver the SHADOW — the signal that creates the gap the audience needs to stay for.**

---

## Cliché Filter & Contextual Specificity Enforcement

Every Wisdom Brief output runs through a validation gate before it reaches Stage 3. This is not optional — it's structural.

### Why Cliché Filtering Is Non-Negotiable

In 2026, generic hooks and universal truths ARE what AI produces by default. Every self-proclaimed expert regurgitates ChatGPT's most probable output. The audience's brain has already associated common taglines, slogans, and generic frames with "AI slop" or "generic guru content." **What we believe is a universal truth, the audience's brain already categorizes as noise.**

The Alchemy is clear:
- **Specificity** bypasses the deception filter (harder to fabricate)
- **Context** makes information absorbable (meaning > data)
- **Story** makes it sticky (narrative > facts)
- **Without all three, content IS disposable**

### The Triple Gate

Each Wisdom Brief output must pass **three tests** before entering Stage 3:

```
GATE 1: CLICHÉ DETECTION
────────────────────────
For each truth claim or statement in the brief:

❌ REJECT if it could appear as a ChatGPT default hook
   Test: "Would a generic AI produce this exact phrase 
   when asked about [topic]?" If yes → it's the average → reject.

❌ REJECT if it's a universal tagline without grounding
   Test: "Can I swap [specific topic] for any other topic 
   and this sentence still works?" If yes → it's generic → reject.
   Example: "The system is rigged" works for finance, 
   healthcare, education, dating → REJECT

❌ REJECT if the audience has heard it from 3+ other sources
   Test: "Is this something gurus in this space commonly say?" 
   If yes → it's background radiation → reject.

✅ PASS only if it's specific enough that:
   - You can't fabricate it on the fly
   - It references a concrete number, event, or sensory detail
   - It smells like something the coach actually KNOWS
```

```
GATE 2: CONTEXTUAL SPECIFICITY
──────────────────────────────
For each truth claim that passed Gate 1:

❌ REJECT if it's disconnected content (information without frame)
   Test: "Does this tell the audience WHAT it means for THEIR life?"
   If it's just a number or stat without consequence → reject.
   Example: "745,000 deaths from overwork" = content (fact)
   "You're trading your health for someone else's profit margin,
   and the WHO counted 745,000 people who paid that price" = context

❌ REJECT if it can't answer "SO WHAT?"
   Test: "Why should THIS person care about THIS data RIGHT NOW?"
   If the brief can't connect the truth to the audience's 
   lived reality → it's disconnected → reject.

✅ PASS only if:
   - The truth is tied to a larger frame the audience LIVES in
   - Meaning, consequence, or causality is explicit
   - The audience can see themselves in the specifics
```

```
GATE 3: NARRATABILITY
─────────────────────
❌ REJECT if it can't be TOLD as a story
   Test: "Can this truth be embedded in a moment, a scene,
   a before/after, or a lived experience?"
   Data stated as data = disposable.
   Data embedded in narrative = sticky.

❌ REJECT if it requires the audience to process raw information
   Test: "Does the audience need to DO WORK to understand why 
   this matters?" Information overload happens when the audience 
   must assemble meaning themselves. The brief must deliver 
   meaning pre-assembled.

✅ PASS only if:
   - The truth can be told, not just stated
   - It encodes meaning, identity, or values
   - A person could retell this to someone else naturally
```

### Enforcement Per Brief

| Brief | Gate 1 Focus | Gate 2 Focus | Gate 3 Focus |
|-------|--------------|--------------|--------------|
| **Deep Wisdom** | Reject timeless "truths" that are just AI-probable slogans | Every finding must connect to audience's CURRENT lived frame | Findings must be narratable as coach's personal discovery |
| **Fresh Wisdom** | Reject generic "trends show" framing | Every data point must answer "so what for YOU, right now?" | Data must be embeddable as a moment or a scene, not a stat |
| **Authenticity** | Reject "I believe in authenticity" self-descriptions | Self-examination must reference specific experiences/decisions | Coach's credibility must be a STORY ("I lived this"), not a claim |
| **Memetic** | Reject generic audience assumptions ("people want freedom") | Emotional architecture must reference specific raw comments | Designed moments must be retellable ("send this to someone who...") |

---

## Pipeline Comparison

### Current Pipeline
```
Research (96 agents) → SoC → Stage 2 (adapt prompt) → Stage 3 (EVERYTHING ELSE)
                                                         ↑
                                                    Stage 3 must:
                                                    - Process research
                                                    - Apply auth protocol
                                                    - Check memetic triggers
                                                    - Follow archetype structure
                                                    - Generate in coach voice
                                                    = 5 COGNITIVE TASKS
```

### Proposed Pipeline
```
Research (96 agents) → SoC → Stage 2 (adapt prompt) 
                                    ↓
                              Stage 2.5 (WISDOM FORGE)
                              Coach processes 4 briefs:
                              ① Deep Wisdom Brief
                              ② Fresh Wisdom Brief
                              ③ Authenticity Introspection
                              ④ Memetic Vibe Signals
                              = ~800 words total
                                    ↓
                              Stage 3 (PURE EXECUTION)
                              Receives: Adapted prompt 
                              + 4 wisdom briefs + Voice DNA
                              Just 2 tasks: Structure + Voice
```

### What Stage 3 Receives (New)

```
ADAPTED PROMPT (~2,000 words)
  Contains: Archetype structure, section reasoning, 
  prompt framework adapted for this topic

WISDOM PACKAGE (~800 words total):
  ① Deep Wisdom: 200 words of processed timeless insight
  ② Fresh Wisdom: 200 words of processed current ammunition  
  ③ Authenticity: 200 words of coach self-examination
  ④ Memetic Signals: 200 words of audience reaction architecture

VOICE DNA (~500 words)

TOTAL: ~3,300 words — ALL pre-processed, ALL coach-voiced
```

vs. current ~5,900 words with raw research + unprocessed protocols.

**Context reduction: 44%. But quality increase: massive** — because every word is processed wisdom, not raw material.

---

## Voice Architecture Enforcement (MCDA Finding)

The MCDA scored all 4 LLM outputs on Voice Fidelity against the Voice Blueprint's 8 dimensions. Best result: Claude at 6/10 (~4 of 8 dimensions). Core problem: **every output sounds like a presenter talking AT an audience, not a coach talking TO you.**

The Voice Blueprint defines a **speaking architecture**, not a vocabulary list:

```
VOICE BLUEPRINT DIMENSIONS → BRIEF OUTPUT REQUIREMENTS:

1. RHYTHM (short-punchy → expansive)
   → Each brief must alternate: short declarative truth → 
     then flowing "here's why" explanation
   → NOT uniform sentence length

2. OPENING PATTERN (strong statement first)
   → Each brief's WEAPON line must OPEN with the strongest claim
   → NOT build up to it

3. INTENSITY ARC (builds on freedom/limitations)
   → Brief outputs should escalate in emotional temperature
   → NOT maintain flat professional tone

4. TRANSITIONS ("But here's the thing," "And that's why")
   → Brief outputs must use the COACH'S transition language
   → NOT generic AI transitions ("Furthermore," "Additionally")

5. RHETORICAL QUESTIONS ("What if you could…?")
   → At least one designed question per brief batch
   → These ARE information gap moments

6. STATUS QUO CHALLENGE (conviction that empowers)
   → Every brief must contain at least one direct challenge
   → NOT agree with the system and offer tips within it

7. EMPHASIS WORDS ("true," "real," "ultimate," "actually")
   → These mark the genuine vs conventional boundary
   → Used to signal "what you think vs what's actually happening"

8. TONE (encouraging yet no-nonsense, earning→creating)
   → The brief must read like the coach REASONING, not REPORTING
   → Intimacy > authority. Coach in your ear > presenter on stage.
```

> [!IMPORTANT]
> **The SoC is the MANIFESTATION of the Voice Blueprint.** When evaluating brief outputs, ask: "Does this read like it came from the same person who produced the SoC?" The SoC has raw urgency, conversational asides, building frustration, and intimate directness. Any brief output that reads like a polished TED talk has failed the voice test — even if every keyword is present.

---

## Answer Machine → Question Machine (MCDA Finding)

The MCDA found that all 4 outputs are **answer machines**: they deliver all truths, resolve all tension, close all gaps. The audience knows everything by the end — which means there's no reason to engage further.

The Alchemy is clear: **the question is always more engaging than the answer.** Great content is a question machine — it holds back resolution, creating tension.

### Gap Design Rules for Stage 2.5

Each Wisdom Brief must explicitly design ONE **information gap** — a place where the truth is signaled but NOT fully delivered:

```
DEEP WISDOM BRIEF → GAP TYPE: "THE MISSING PIECE"
   Signal the revelation. Don't complete it.
   "Everyone knows X, but nobody asks WHY X happens to the 
   people who do everything right."
   The brief gives Stage 3 the SIGNAL, not the ANSWER.
   Stage 3 uses this to create the moment where the audience 
   leans forward.

FRESH WISDOM BRIEF → GAP TYPE: "THE BURIED LEAD"
   Bury the most alarming data point in a contextual frame.
   "The number everyone should be watching isn't [obvious metric] — 
   it's [specific obscure metric] and here's what it just did."
   The brief gives Stage 3 the DATA that creates urgency,
   but frames it as something the audience DIDN'T KNOW TO LOOK FOR.

AUTHENTICITY BRIEF → GAP TYPE: "THE DOCTRINE IN ACTION"
   The coach shows the FEELING (vulnerability) → then the 
   ACTION DESPITE IT (discipline) → then the RESULTS.
   "I felt exactly what you're feeling right now — the fear,
   the hesitation. But I had a system. And I followed it 
   anyway. Here's what happened..."
   The brief gives Stage 3 the three-part move:
   FELT IT → DID IT ANYWAY → RESULTS.
   The gap is emotional: the audience connects because the 
   expert felt the same thing they feel — and the doctrine 
   won. You CAN'T demonstrate competence without showing 
   both sides.

MEMETIC BRIEF → GAP TYPE: "THE WHISPER"
   Design a moment that makes the audience want to TELL someone.
   "Send this to the person who..."
   The gap is social: the audience can't resolve the emotion alone.
   They need to share it to complete the circuit.
```

### The Anti-Answer Rule

> [!CAUTION]
> **If a brief output ANSWERS everything, it has failed.** The brief should give Stage 3 ammunition to create tension — not ammunition to resolve it. Stage 3's job is to build a question machine. Stage 2.5's job is to design the questions.

---

## Open Questions for This Architecture

### MCDA-Informed Insights

The 4-model comparison revealed patterns that narrow some of these questions:

1. **Is Stage 2.5 a separate session or part of Stage 2?**
   - Separate session = cleaner cognitive isolation
   - Part of Stage 2 = less pipeline overhead, natural Phase B.5
   - **MCDA insight:** The outputs that scored highest (Claude, Gemini) were the ones that absorbed the SoC most faithfully. This suggests voice processing benefits from isolation — if Stage 2.5 runs in the same session as Stage 2's structural reasoning, voice may get contaminated by structural thinking. Lean toward **separate session**.

2. **Order of the 4 briefs — does it matter?**
   - Authenticity first (ground in who you are) → Research wisdom (process knowledge) → Memetic last (design for audience)
   - Or: Research first → Authenticity (filter through values) → Memetic (optimize for spread)
   - **MCDA insight:** Gemini's one genuine wisdom line ("radical act of Ownership & Control") emerged when research was filtered THROUGH the coach's vocabulary. This suggests: **Authenticity first** (establish voice), then research wisdom (filter through voice), then memetic (design for audience). Voice is the lens, not the decoration.

3. **Does Brief 4 (Memetic) absorb or replace AIP Phase C?**
   - Currently: AIP processes comments per dimension (14 × 5 lenses)
   - Proposed: Memetic brief processes comments through 5 lenses including Information Gap Design
   - These are DIFFERENT lens structures — could they coexist or is it redundant?
   - **MCDA insight:** None of the 4 outputs used audience signal. The AIP processing didn't reach Stage 3 in the monolith test. This suggests the Memetic Brief should be the ONLY audience signal processor — absorbs AIP Phase C entirely. Simplify, don't duplicate.

4. **200 words per brief enough?**
   - 4 × 200 = 800 words total wisdom
   - The research briefs being absorbed are ~2,400 words combined
   - Compression ratio: 2,400 → 800 = 67% — is that too aggressive?
   - **MCDA insight:** Claude's best moments were SINGLE SPECIFIC DATA POINTS with context ("Housing Affordability Index fell below 100 + translation"). One specific contextual truth > 200 words of generic content. **200 words is enough IF every word passes the Triple Gate.** The problem is never word count — it's word quality.

5. **Should the 4 briefs have a unified lens structure?**
   - Currently each has its own 5 questions
   - Should they all use the same WIP lenses?
   - Or are domain-specific lenses more effective? (Current choice: domain-specific, each governed by relevant Alchemy principles)
   - **MCDA insight:** The Truth Recognition taxonomy (5 types) suggests each brief naturally maps to different recognition types. Domain-specific lenses are the right call — but ALL lenses must pass through the same Triple Gate (cliché, contextual specificity, narratability).

6. **Where does the three-part vulnerability move land structurally in the final script?**
   - The Authenticity Brief produces the FELT IT → DID IT ANYWAY → RESULTS sequence
   - But WHERE in the script template does this beat appear?
   - **MCDA insight:** All 4 outputs are pure expert mode — none acknowledge the feeling, none show the action despite it, none provide results as proof. This suggests the three-part vulnerability move needs a STRUCTURAL slot in the archetype template.
   - **User Guidance:** "Competence is the Art of Attracting. Vulnerability is for Retention." You can't lead with vulnerability if there's no trust.
   - **Proposed:** **"Doctrine in Action" beat is part of the Retention Phase (after the Body/Competence section).** The coach hooks with competence/insight (Attraction), establishes authority, THEN uses the specific "doctrine in action" story to lock in retention and emotional memory before the Call to Action.

7. **How do we enforce Voice Blueprint's 8 dimensions in brief outputs?** (NEW)
   - The MCDA proved that keyword presence ≠ voice. Gemini had all the metaphors but still scored only 5/10 on voice fidelity.
   - **Options:**
     - A: Include Voice Blueprint dimensions as structural requirements in each brief's prompt
     - B: Add a Voice Architecture validation pass (separate from Triple Gate)
     - C: Make the SoC the primary voice reference and instruct briefs to "match the rhythm and temperature of the SoC"
   - **Lean toward C** — the SoC is already the manifestation of the blueprint. Saying "match the SoC" is more concrete than "follow 8 abstract dimensions."

---

*Brainstorm 2 (v4): Stage 2.5 produces 4 pre-processed wisdom briefs governed by 7 Alchemy principles | Triple Gate cliché filter | 5-type Truth Recognition taxonomy | Voice Architecture enforcement (8 Blueprint dimensions) | Answer→Question Machine gap design per brief | MCDA-informed open questions with proposed answers | Context: 5,900 → 3,300 words*


---

## I-R-E-V-C Session Protocol

### INGEST
- Load adapted prompt from Stage 2
- Load deep + fresh research briefs
- Load vibe_comments_processed.json
- Load coach_soul.json

### REASON
- Generate 4 specialized wisdom briefs using WIP (Wisdom-Infusion Protocol) lenses:
  1. Research Synthesis Brief - Fuses deep + fresh research into actionable insights
  2. Audience Pain Brief - Extracts the most potent audience pain points from vibe_comments
  3. Voice Calibration Brief - Fine-tunes the adapted prompt's voice alignment
  4. Story Architecture Brief - Maps the narrative structure for maximum emotional impact
- Each brief applies WIP lenses:
  - Transform knowledge -> wisdom (not just facts, but meaning)
  - Apply coaching perspective (what would the coach say about this?)
  - Connect to audience lived experience (not abstract, but felt)
- Each brief <= 200 words (concise, actionable)

### EMIT
- Output wisdom_briefs.json with 4 brief objects

### VALIDATE
- 4 briefs present (Research Synthesis, Audience Pain, Voice Calibration, Story Architecture)
- Each brief <= 200 words
- Each brief connects research findings to audience lived experience
- No brief is just a summary - each must add the "wisdom" layer

### CHECKPOINT
- Update config.yaml: sessions.production.wisdom_forge.status = "complete"
