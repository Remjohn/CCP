# Law 28: The Conscious Elite — CBCS Program Architecture Brief (Draft 1)

**Date:** April 2026
**Author:** CCP Architecture Team
**Classification:** Internal Engineering Brief — Pre-PRD
**Word Target:** 3,200 – 3,600 words

---

## 1. Purpose & Mandate

This document formalizes how the **Law 28 / Conscious Elite** 28-Day Voice Crucible maps onto the existing **Conscious Behavioral Change System (CBCS)** infrastructure. The core insight driving this brief is that the Law 28 program is not a separate product. It is a **CBCS program instance** — the exact same Identity Engineering architecture (Assessment → Assembly → Priming → Action → Evidence → Shift) that coaches will deploy for their own clients. The only structural difference is the container into which the output data flows.

This document covers three operational layers:

1. **CBCS Update Brief** — How the existing 4-Engine architecture adapts for the Law 28 schema.
2. **Dashboard Update Brief** — What the Coach sees vs. what we see internally.
3. **Telegram Command Layer** — The slash commands that let the coach (and us, as the architect) operate the transformation engine without ever opening a dashboard.

---

## 2. The Unified CBCS Model: Why Law 28 Is Just Another Program

### 2.1 The Universal Self-Coding Paradigm

The CBCS product brief establishes that the system treats daily rituals as "Training Data" that fine-tunes the user's identity (the LoRA analogy). In the existing architecture, the user performs a behavioral ritual (breathwork, journaling, cold shower) and the system captures "Evidence" — voice notes, completion signals, streak data — which updates the Neo4j Context Premise graph.

This principle must be **universal across every CBCS program** — not just Law 28. Every program interaction generates richer structured data about the participant than any intake questionnaire could ever capture. A 28-day program produces 28 voice recordings, 28 transcripts, 28 biometric snapshots, and hundreds of Context Premise entity extractions. By comparison, an onboarding form captures maybe 12 data points on a good day.

For the Law 28 program specifically, the "Training Data" is a **communication act**. Every day, the participant records content: a 2-minute counter-narrative, a 60-second pitch, a vulnerability hook, a comedic reframe. This recording is simultaneously:

- **Proof of Change (The Evidence):** The FR61 Voice Coach scores Conviction Density, Pause Architecture, Hedging Frequency, and Pitch Stability. These biometric scores update the user's Voice DNA profile over the 28 days, creating an undeniable, data-backed arc of transformation.
- **Content Production (The Byproduct):** Every recording is also a usable content asset. The CMF Trivela Auto-Renderer can process these raw audio files into branded carousels, audiograms, and short-form video. The user walks out of 28 days with 28 pieces of content and a measurably stronger voice.
- **Actionable Intelligence (The Strategic Dividend):** Every transcript, every Context Premise update, every emotional state captured by Aria becomes **queryable, targetable, and deployable data**. The coach (or the platform architect) can later command the system: "Find every participant who expressed fear of pricing conversations and generate a webinar script that addresses their exact objections." This is the difference between a dead questionnaire and a living intelligence system.

This is the "Self-Coding" paradigm: the act of completing the challenge IS the act of programming the machine. The user doesn't fill out forms; they speak, and the system listens. The more they participate, the smarter the system becomes about them — and the more precisely the coach can serve, target, and convert them.

### 2.2 Three-Layer Context Premise Architecture (Critical Correction)

This is the most important engineering distinction in the entire brief. There are **three distinct Context Premise containers** in the CCP/CBCS ecosystem. Confusing them is an architectural failure.

#### Layer 1: The Conscious Elite Context Premise (OUR Marketing Intelligence)

When **coaches** participate in the Law 28 program, they are OUR clients. Their Context Premise data — their fears, frustrations, enemies, hidden beliefs, success markers — feeds the **Conscious Elite Marketing Engine**. This data belongs to us. It tells us what coaches struggle with, what language they use to describe their pain, what objections they have about scaling, what competitors they secretly envy. This intelligence powers:
- Our own ad copy and promotional flyers (rendered via CPSC → Skia pipeline)
- Our own webinar scripts ("We know 73% of you are afraid to charge more than $200/session — here's why that's costing you $400K/year")
- Our own sales page optimization
- Our Swarm Intelligence for improving the Law 28 curriculum itself

> **This data has NOTHING to do with what's inside the coach's CCP container.** The coach's CCP container is their business tool. The Conscious Elite Context Premise is our intelligence about them as customers.

#### Layer 2: The Coach's CCP Container (Fed by Their Clients)

When **regular clients** (end-users) participate in a coach's CBCS program, their Context Premise data feeds the **coach's CCP container**. This is the coach's business intelligence. It tells the coach:
- What their clients fear, envy, dream about
- How their clients describe their own struggles (in their raw voice, not marketing language)
- Which persuasion layers work best on which client segments
- Which drills produced the biggest breakthroughs

This data makes the coach's CCP system smarter over time. The more clients they run through programs, the richer their Neo4j graph becomes, the more precise their Digital Stunt Double, and the more accurate their CMF Trivela output.

#### Layer 3: The Universal Voice DNA Stream

Regardless of Layer 1 or Layer 2, every participant's voice recordings (when applicable) feed the **Voice DNA pipeline (FR3)**. For coaches, this enriches their personal Voice DNA profile — improving their Digital Stunt Double's prosody, metaphors, and cadence. For regular clients, Voice DNA data stays within the coach's tenant boundary and is used solely for Context Premise entity extraction (not voice cloning).

#### The Routing Matrix

| Participant Type | Context Premise → | Voice DNA → | Content Assets → | CPSC Promotional → |
|---|---|---|---|---|
| **Coach in Law 28** | Layer 1 (Conscious Elite marketing) | Coach's personal FR3 profile | Coach's CCP Content Library | OUR promotional pipeline |
| **Client in Coach's CBCS Program** | Layer 2 (Coach's CCP container) | Coach-tenant entity extraction only | N/A (private evidence) | Coach's CPSC pipeline |

This routing must be enforced at the API middleware level. The routing decision is based on two fields: `user_role: coach|client` and `program_owner_id` on the user profile. The middleware inspects these before forking the ingestion pipeline.

### 2.3 Reference Academic Frameworks

The following frameworks from the existing CBCS Intelligence Library and the CCP PRD directly support the Law 28 program design:

| Framework | Source | Application in Law 28 |
|---|---|---|
| **Self-Perception Theory** (Daryl Bem) | CBCS Product Brief §3.1 | The coach observes themselves speaking with conviction → infers they ARE a bold communicator. The 28 days of audio evidence "denoise" their self-image. |
| **Cognitive Dissonance** | CBCS Product Brief §3.1 | The gap between "I am an expert" (Goal) and "I hesitate before hitting record" (Identity) is the exact chaos we resolve. |
| **Social Penetration Theory** | CCP PRD, Capability Area 9 | The progressive vulnerability structure of Law 28 (Week 1: surface → Week 4: deep conviction) mirrors SPT's onion-layer model. Each week peels a deeper layer. |
| **Cognitive Appraisal Theory** | CCP PRD, FR3 Voice DNA | The FR61 engine uses CAT to measure not just what the coach says but how they emotionally appraise their own claims. Conviction Density IS a CAT metric. |
| **LIWC-22 Markers** | CCP PRD §Voice DNA | Linguistic Inquiry Word Count markers detect hedging language ("I think," "maybe," "sort of"), which are the biometric signatures of timidity. Law 28 trains their elimination. |
| **Computational Stylometry** | CCP PRD §Voice DNA | Tracks sentence length variation, vocabulary richness, and syntactic complexity across the 28 days. A growing Stylometric Diversity Score indicates the coach is escaping verbal ruts. |
| **The 9-Layer Persuasion Cycle** | CBCS Intelligence Library (persuasion_layers.yaml) | Layer 2 ("The Challenger") is the default persuasion angle for Law 28. The AI accountability partner uses Constructive Tension as the primary mechanism. |
| **Identity Threat Taxonomy** | CBCS Intelligence Library (identity_threat_taxonomy.yaml) | Identifies the specific ego-protection mechanisms that cause coaches to soften their language. Law 28 targets these directly. |
| **Self-Determination Theory (SDT)** | CBCS Intelligence Library (sdt_markers.yaml) | Tracks Autonomy, Competence, and Relatedness — the three pillars of intrinsic motivation. Law 28 must deliver a WIN on all three by Day 7 to prevent early churn. |

---

## 3. Program Structure: The Adaptive Architectural Layers

### 3.1 The Adaptive Milestone Architecture (The "28-Day" Hook)

The classic coaching mistake is separating curriculum into rigid chronological blocks or distinct "programs" (e.g., "Week 1 is X, Week 2 is Y"). The CBCS rejects this. "28 Days" is our marketing hook to drive upfront commitment, but the actual execution is a **dynamically gated progressive architecture**. 

Timing is highly personalized for each milestone. A participant progresses from foundational milestones to advanced layers only when their biometric data (FR61) and Context Premise show they have cleared their current weakness. If a client is crippled by "hedging language," they do not advance to the "Challenger Reframe" just because it is Tuesday. The system dynamically generates intervention drills until the biometric weakness is resolved. This is the difference between having an accountability buddy and being guided by a sovereign digital coach.

### 3.2 Daily Persuasion & The Sunday Postcard

We do not "sell" the challenge once at checkout. We must re-sell the transformation to them *every single day* so they are pumped to act on their own personal reasons, pains, and aspirations. 

- **Daily Persuasion:** Every daily drill prompt is prefixed with a personalized "Why" generated by the Neuro-Persuasion Engine, explicitly referencing the client's own Context Premise. They aren't doing a drill because it's in the curriculum; they are doing it because *they explicitly told the system they wanted to stop feeling invisible*.
- **The Sunday Postcard:** Every Sunday, the participant receives an auto-generated visual "Postcard" report via Telegram. This is not a bland progress bar. It includes a **highly challenger, opinionated comment** from the AI Coach based on their week's data. *(Example: "Your conviction density improved by 14%, but your pitch stability collapsed at the end. You're still speaking like you need permission to be in the room. This week, we stop asking for permission.")*

### 3.3 The Progressive Architectural Layers

Instead of 12 disconnected programs, the CBCS builds one continuous capability stack. Participants are mapped against their weaknesses via the initial diagnostic and ongoing daily testing, meaning two users will experience radically different paths through the layers.

**Layer 1: The Foundation (Boldness + Conviction)** 
The non-negotiable base. Establishing Voice DNA baseline, eliminating apology/hedging language, and surviving the terror of unscripted recording. (Usually clears in Milestones 1–7).

**Layer 2: The Structure (Pitch & Reframe)**
Once the foundation is biometrically solid, the system attacks structural weakness: High-Ticket Framing, leading with tension instead of pleasing, and using the Challenger methodology.

**Layer 3: The Nuance (Narrative & Comedy)**
Adding depth. Mining personal history for The Lived Story, integrating the Jim Rohn Prosody Engine (pauses, comedic timing, tension-release), and learning to speak "to one person" in DMs.

**Layer 4: The Sovereign Command (Stage & Crisis)**
Full interactive mastery. Live objection handling, holding the frame under attack, Trivianar execution, and capstone 12-minute extemporaneous keynotes. 

*Because this is adaptive, a client with high natural charisma but terrible sales framing might fast-track through Layer 1 and spend 15 milestones grinding through Layer 2. The CBCS solves the human, not the calendar.*

### 3.4 Weekly Touchpoints (Non-Negotiable)

Beyond the 6 daily drills, the program enforces three synchronous touchpoints:

1. **6x/week — Accountability Partner Check-In (Telegram):** Each participant is paired with one other participant. They exchange voice notes reviewing each other's daily drill. This is the Galloway "friendship retention" lever. If they make a friend, they don't leave.
2. **1x/week — Group Event (Telegram Group Call / Trivianar / Q&A):** A live session where participants perform their drills in front of the cohort. Public execution forces boldness in a way private recordings cannot. This can take the form of a Q&A, a live Trivianar game, or a coaching hot-seat. The format rotates.
3. **1x/month — Outside Event (IRL or Virtual Intensive):** A high-stakes event outside the Telegram container. This could be a virtual masterclass with a guest speaker, a live "Speak-Off" competition, or an IRL meetup. This prevents the program from becoming a "digital bubble" and anchors the transformation in the physical world.

### 3.5 Audit-First Onboarding: The Free Assessment → Trial → Conversion Funnel

The classic coaching mistake is asking someone to pay before they understand themselves. The CBCS reverses this. The user's journey begins with a **free, algorithmically built voice assessment** — and they receive their results as a Telegram Voice Note, not a PDF. This immediately places them inside the CBCS invisible app paradigm *before they've spent a dollar*.

#### The Flow

```
Step 1: FREE ASSESSMENT (Telegram Bot)
   User clicks a link → lands in Telegram → takes a 3-minute voice assessment
   (record a 60-second pitch, answer 3 voice prompts)
   ↓
Step 2: VOICE NOTE RESULTS (FR61 + Aria)
   The system scores their recording via FR61 (Conviction Density, Hedge
   Frequency, Pause Architecture, Pitch Stability) and Aria extracts their
   Context Premise. Results are delivered as a PERSONALIZED TELEGRAM VOICE
   NOTE — not a generic scorecard. The AI Coach tells them, in the coach's
   Voice DNA, exactly where they are weak and why it's costing them.
   ↓
Step 3: 7-DAY CHALLENGE (Credit Card Required)
   "Your conviction density is at 34/100. Most coaches who command premium
   rates score above 70. Want to fix this in 7 days? Start the free trial."
   The user MUST enter credit card info to enroll ($0 for 7 days, auto-billed
   afterward). This adds upfront friction but creates high-intent commitment.
   ↓
Step 4: THE "SILENT SALES" CHALLENGER APPROACH (Days 1–7)
   We do not hard-pitch them to buy. Instead, the coach uses the intelligence
   gathered to reach out personally via Telegram DMs, inviting them to hang
   out at a group event (Trivianar, Q&A). The coach demonstrates blunt, 
   Challenger-style authority, making the user *feel* the value viscerally 
   so they willingly let the auto-charge process on Day 7.
```

#### Why This Is Devastating Commercially

The assessment itself is the Audit Engine. It does three things simultaneously:

1. **It qualifies the lead.** Anyone who won't record a 60-second voice note is not a serious coaching prospect. Self-selection eliminates tire-kickers before we spend a cent.
2. **It seeds the Context Premise graph.** Even a single 60-second recording gives Aria enough to extract fears, hedging patterns, and identity signals. The CCP already knows more about them than their Instagram bio.
3. **It creates the undeniable proof.** When the voice note comes back saying "You used the word 'just' 7 times in 60 seconds — that's why your audience scrolls past you," the user cannot un-hear it. The Otis Elevator Demonstration fires before they've paid anything.

### 3.6 The B2B2C Payment Architecture: Coach-Pays Model

This is the critical commercial innovation. **The end-user never pays us directly.** The coach pays us per user via Stripe metered billing — the same infrastructure already specified in the AFFiNE Billing Architecture (FR-COM-01).

#### The Revenue Matrix

| User State | What Happens | Coach Charged | End-User Pays |
|---|---|---|---|
| **Assessment** | User takes free voice assessment via Telegram | $0.00 | $0.00 |
| **7-Day Trial** | User enrolled in free trial challenge | **$1.90** per trial user | $0.00 |
| **Paid Client** | User converts to full program after trial | **$3.90** /user/month | Coach decides (their pricing, their Stripe) |

#### Why Coaches Will Pay $1.90 Per Trial User

The $1.90 is not a cost — it is the cheapest qualified lead in the coaching industry. Consider:

- **Facebook/Instagram ads** cost $5–$15 per lead, and those leads are cold — name + email, zero behavioral data.
- **Our $1.90 trial user** arrives with: a voice recording, an FR61 biometric snapshot, a Context Premise extraction (fears, hedging patterns, identity signals), 7 days of daily engagement data, an accountability partner relationship, and a Change Talk Vault with commitment language.

By the time the trial ends, the coach's CCP knows more about that person than 3 discovery calls would reveal. The $1.90 buys intelligence, not just a name.

#### Why $3.90/Month Per Paid Client Works

This is consistent with the existing billing architecture (previously $4.00/user in the AFFiNE Billing spec). The slight reduction to $3.90 creates psychological pricing continuity with the $1.90 trial tier. At scale:

| Coach Scale | Trial Users/Month | Conversions (40%) | Monthly Platform Cost | Coach Revenue (at $197/client) |
|---|---|---|---|---|
| Small (10 trials) | 10 | 4 | $19 + $15.60 = **$34.60** | $788 |
| Medium (50 trials) | 50 | 20 | $95 + $78 = **$173** | $3,940 |
| Large (200 trials) | 200 | 80 | $380 + $312 = **$692** | $15,760 |

The unit economics are absurd. Even the large coach paying $692/month is getting 200 qualified, psychologically profiled leads and 80 paying clients for less than half a Facebook ad budget.

#### Stripe Implementation: Dual Metered Line Items

The existing Stripe Subscriptions with Metered Billing architecture (FR-COM-01) already supports this. We add **two metered line items** to the coach's subscription instead of one:

```
Coach Subscription:
├── Base Plan: $0 (or optional base tier)
├── Metered Item 1: "Trial User Credits" → $1.90/unit
│   └── Usage Record reported when: trial user completes Day 1 assessment
└── Metered Item 2: "Active Client Credits" → $3.90/unit
    └── Usage Record reported when: trial user converts to paid (Day 7+)
```

**Billing Rules:**
- Trial usage is reported the moment the user completes their **first voice assessment** (not when they click the link — prevents bot abuse).
- Active client usage is reported when the user **completes the 7-day trial AND the coach confirms conversion** (or auto-converts if the user opts in).
- If a trial user churns (doesn't convert), the coach was charged $1.90 — they keep the intelligence data (Context Premise, Voice DNA snapshot) forever. The lead is not wasted.
- The existing Redis Permission State cache and webhook reconciliation from FR-COM-01 apply unchanged.

#### The Conscious Elite Layer: Our Own Revenue

When coaches themselves are participants in OUR Law 28 program (Layer 1 of the Three-Layer Architecture), the same model applies but in reverse — **we** are the coach, and **they** are our trial users. Our Conscious Elite marketing intelligence accumulates their data while they experience the program. This creates a perfect closed loop:

1. Coach takes our free assessment → we learn their fears and weaknesses
2. Coach enters our 7-day trial → we accumulate 7 days of voice data
3. Coach converts to paid Law 28 → we charge them directly (not per-user, but program pricing)
4. Coach graduates → activates their own CCP → we charge them $1.90/$3.90 per THEIR users
5. Their users' data feeds Layer 2 (coach's container) while our coach data feeds Layer 1 (our marketing intelligence)

**The flywheel:** More coaches → more trial users → more data → better intelligence → better marketing → more coaches.

### 3.7 Acquisition Expansion: The "Silent Referral" Viral Loop

The acquisition funnel ($1.90 trials / $3.90 conversions) does not rely solely on paid ads or cold outreach. By leveraging the Telegram Mini App architecture internally, we deploy a **Notcoin-Style Viral Loop** directly inside the habit tracker.

**How the "Silent Referral" Works:**
Because identity resolution in Telegram is instantaneous (no "create an account" steps), sharing is frictionless. The Mini App embeds native viral mechanics:
1. **Social Accountability Multipliers:** Users are prompted to "Do it with a friend." If they invite a contact via Telegram's share sheet, and both users complete their daily drill/Pomodoro, both receive a **Streak Multiplier**. 
2. **Feature Unlocking:** High-value modules (like the WebRTC Sales Roleplay Room) are paywalled. Users can either pay $9.00 outright, OR unlock it natively by successfully inviting 2 friends into the free tier.
3. **Micro-Leaderboards:** Friends can create local 3-person leaderboards, establishing hyper-localized peer pressure that locks them into the ecosystem.

This gamified referral system allows the CBCS to act as an autonomous customer acquisition engine for both the Coaches (their clients refer friends) and Conscious Elite (coaches refer other coaches).

---

## 4. Dashboard Update Brief: The Coach's View

### 4.1 Lean Dashboard Mandate

The coach dashboard for any CBCS program — including Law 28 — must follow the **Lean Cognitive Load** principle. The coach does not need to see the FR61 biometric waterfall, the LIWC-22 markers, or the Neo4j Context Premise graph. They need to see:

| Dashboard Element | What It Shows | Data Source |
|---|---|---|
| **Client Card** | Name, Photo, Current Level, Current Day (e.g., "Day 14 of 28") | Supabase user profile |
| **Progress Ring** | Visual completion percentage for the current level | Supabase ritual_logs |
| **Streak Flame** | Current consecutive-day streak | Redis counter |
| **Conviction Score** | Single composite number (0–100) derived from FR61 Conviction Density, Hedge Frequency, Pitch Stability | FR61 engine → simplified composite |
| **Mood Indicator** | Current TTT state (color-coded: Green = confident, Yellow = hesitant, Red = distressed) | Aria's latest Context Premise extraction |
| **Red Flag Feed** | Clients who missed 2+ consecutive days or whose TTT dropped below threshold | Liliane (Empathy Agent) alerts |
| **Intercept Button** | "Send Personal Voice Note" — pauses the AI loop and opens a direct Telegram recording | Telegram Bot API |

### 4.2 What We See Internally (The Full Intelligence Layer)

Behind the coach's lean dashboard, the CCP internal analytics layer tracks the full spectrum of CBCS intelligence:
- FR61 biometric time-series (daily Conviction Density, Pause Architecture, Jitter, Shimmer, Hedge Frequency)
- Voice DNA evolution curves (LIWC-22 marker trajectories, Stylometric Diversity Score)
- Context Premise graph (Neo4j visualization of Fears, Enemies, Hidden Beliefs, and how they shift over the 28 days)
- Swarm Intelligence data (aggregate patterns across all Law 28 participants — which drill types produce the highest conviction gains)

This data feeds the Learning Optimization Board for continuous program improvement.

---

## 5. Telegram Command Layer — The Definitive 28-Command Intelligence Suite

> **Design Principle:** Every command below was derived by auditing the CCP/CBCS/CPSC architecture and asking: *"What queryable data already exists in the system that, if surfaced at the right moment via a simple slash command, would give the coach an outsized strategic advantage?"* Each command cites the exact `DEP-ID` or `FR` module it integrates with.

### 5.1 Tier 1: Participant Commands (6)

These commands are available to any user enrolled in a CBCS program (including Law 28):

| # | Command | Function | Data Sources |
|---|---|---|---|
| 01 | `/today` | Returns today's drill prompt, contextualized with the participant's latest FR61 biometric snapshot (if Hedge Frequency spiked yesterday, today's drill targets hedging). Includes accountability partner feedback. | FR32 Atlas Roadmap, FR61, Supabase ritual_logs |
| 02 | `/submit` | Initiates the voice recording flow. Audio is transcribed (Groq Whisper), scored (FR61 Conviction Density + Pause Architecture + Hedge Frequency), and entities are extracted (Aria → Neo4j). One button triggers 4 parallel intelligence pipelines. | Epic 1.3, FR29, FR61, FR-CBCS-09 |
| 03 | `/progress` | Returns current streak, level, day count, and a 7-day Conviction Score trendline (text sparkline). | Redis streak, FR61 composite, Supabase user_program |
| 04 | `/partner` | Shows accountability partner info + their latest drill (audio + FR61 score) for peer review. The Galloway retention lever — social visibility creates reciprocal obligation. | Supabase partner pairing, FR61 |
| 05 | `/reflect` | Triggers the guided journal prompt (rest days). Response is processed by Aria for Context Premise extraction and Change Talk Vault capture. | Intelligence Library, FR29, FR-CBCS-01 |
| 06 | `/score` | Returns full FR61 biometric breakdown: Conviction Density, Hedge Frequency, Pause Architecture, Pitch Stability, Stylometric Diversity, and the 28-day delta. The "Otis Elevator Demonstration" — undeniable proof. | FR61, FR47 LIWC-22, FR3 Voice DNA |

### 5.2 Tier 2: Coach Operations Commands (6)

These commands give the coach Telegram-native control of their program without ever touching a dashboard:

| # | Command | Function | Data Sources |
|---|---|---|---|
| 07 | `/cohort` | Returns a formatted summary of ALL active participants: Name, Day, Streak, Conviction Score, TTT Mood State (color-coded), Red Flag status. | FR32, FR61, FR18, Liliane (FR-CBCS-14) |
| 08 | `/intercept [user]` | Pauses the AI coaching loop for a specific participant. Coach records a personal voice note sent directly via Telegram. AI resumes after `/resume [user]`. The human override when Liliane detects crisis. | FR39 Emilio Orchestrator, Telegram Bot API |
| 09 | `/broadcast [message]` | Sends a text or voice message to ALL participants in the current cohort. | Telegram Bot API, Supabase |
| 10 | `/redflags` | Returns ONLY the participants flagged by Liliane: missed 2+ consecutive days, TTT dropped below threshold, or Conviction Score regressed >15% from peak. | FR-CBCS-14 Liliane, FR61 regression detection, FR-CBCS-09(FR30 Dormancy Recovery |
| 11 | `/stats` | Returns aggregate program metrics: avg. Conviction Score delta (Day 1 → current), retention rate, completion rate, most effective drill (by conviction gain), most dropped drill (by skip rate), cohort-wide Hedge Frequency trend. | FR61 aggregate, Swarm Intelligence, Supabase ritual_logs |
| 12 | `/event [date] [type]` | Schedules the weekly group event (Q&A, Trivianar, Hot Seat). Sends calendar pings with personalized context per user (e.g., "This week's Trivianar focuses on pricing fear — you mentioned this on Day 9"). | FR29 Neo4j, FR-CA11-19 Trivianar Engine, Bot API |

### 5.3 Tier 3: Sales & Marketing Intelligence Commands (8)

This is the category that transforms the CBCS from a "program runner" into a **Strategic Intelligence Engine**. Each command reaches into the 7 CBCS intelligence modules (Change Talk Vault, ICT Mapper, SPT Gauge, TII, SEARCH Phase, Voice DNA, Context Premise) and the CPSC sales pipeline (FR51–FR60).

| # | Command | Function | Pipeline Integration |
|---|---|---|---|
| 13 | `/segment [criteria]` | Queries the Neo4j Context Premise graph for clients matching specific psychological criteria. Example: `/segment fear:pricing AND identity:Rebel AND coping:>=3`. Returns a psychologically precise audience slice built from 28 days of raw voice data — not self-reported checkboxes. | FR6, FR29 (Neo4j), FR-CBCS-04 (ICT), FR-CBCS-02 (SPT), identity_pillars.yaml |
| 14 | `/webinar-brief [segment] [topic]` | Generates a full webinar conversion brief (FR52) hyper-targeted to the segment. Queries Change Talk Vault for verbatim commitment phrases, segments webinar modules by the tribe's modal Coping Position, and validates through the Structural Coping Alignment Gate. | FR52 (full pipeline), FR-CBCS-01 (Change Talk verbatim), FR-CBCS-04 (module segmentation) → Output: DEP-ENG-073 for FR33 V²WS |
| 15 | `/invite-list [segment] [event_id]` | Generates a ranked list of participants per segment, each with a personalized invite referencing their specific Context Premise data. "Sarah, you told us pricing conversations make you anxious. Thursday's session addresses exactly that." Ranks by FR55 4-signal convergence. | FR55 (4-signal), FR53 (vulnerability calibration), FR29 (Neo4j nouns), FR-CBCS-06 (SEARCH) |
| 16 | `/conversion-pulse [segment]` | Returns real-time sales readiness per segment member. Shows 4-signal convergence: Coping Position, SPT Stage, TII Composite, SEARCH Phase. Clients at `HIGH_CONFIDENCE_READY` (all 4 signals converged) are highlighted. Signal Detection Theory applied to sales. | FR55, FR-CBCS-04, FR-CBCS-02, FR-CBCS-07, FR-CBCS-06 |
| 17 | `/ad-copy [segment] [platform]` | Generates platform-specific ad copy (Instagram, Facebook, YouTube, TikTok) using the segment's own language from Context Premise entities. Tribal noun injection via Character Lexicon, DHD formula from the Intelligence Library. No clichés — their exact words. | Neo4j (FR6), FR0C (Character Lexicon), persuasion_layers.yaml, FR3.4 (Artisan TTT-calibrated) |
| 18 | `/social-proof [segment]` | Retrieves psychologically matched testimonials via FR57's 3-point homophily filter (Coping + SPT + Identity Pillar). Shows Position 2 clients success stories from other Position 2 clients — not millionaire Position 5 testimonials that alienate beginners. | FR57 (full pipeline), DEP-ENG-024 (Coach Story Archive), Relevance Stringency Gate |
| 19 | `/offer-check [segment] [tier]` | Pre-validates whether a specific offer tier can be safely sent to a segment. Runs FR58 Upward-Only Routing Gate and FR-CBCS-12 Commercial Matrix Routing Gate. Returns breakdown: X PASS, Y PROVISIONAL (require manual approval), Z FAIL (capacity exceeded — will NOT receive offer). | FR58 (Offer Tier), FR-CBCS-12 (Coping Matrix Gate), FR-CBCS-04 (ICT), Stripe via FR45 |
| 20 | `/loom-report [campaign_id]` | Generates a full Loom Intelligence Narrative (FR60) for a completed campaign. Explains *why* the campaign succeeded or failed based on Coping Positions and Change Talk data. Anti-hallucination regex gate prevents generic marketing advice — every recommendation traces to a defined matrix shift. | FR60 (full pipeline), FR56 (Campaign Registry), Actionable Threshold Gate |

> **The Vision in Action:** The coach types `/segment fear:pricing AND coping:>=3` → gets 23 matches. Types `/webinar-brief segment:pricing-fear "Why You're Undercharging"` → gets a complete script with verbatim Change Talk quotes. Types `/invite-list segment:pricing-fear event:thursday-trivianar` → gets 23 personalized Telegram invites. Types `/flyer segment:pricing-fear offer:Law28-L2` → gets a Skia-rendered visual asset for fishing in the wild. Types `/offer-check segment:pricing-fear tier:2` → "19 PASS, 3 PROVISIONAL, 1 FAIL (capacity exceeded)." Types `/conversion-pulse segment:pricing-fear` → "7 clients at HIGH_CONFIDENCE_READY." **That is the CCP competitive moat.**

### 5.4 Tier 4: Content & Asset Production Commands (4)

These commands produce tangible marketing assets via the CPSC/Skia pipeline:

| # | Command | Function | Pipeline Integration |
|---|---|---|---|
| 21 | `/flyer [segment] [offer]` | Triggers the full CPSC → Skia rendering pipeline: Z-Pattern layout, Payload Completeness Gate, ConsciousPose/ConsciousSmile overlays, DHD formula copy from segment's Context Premise. Output: production-ready visual asset. | FR54, Skia renderer (src/skia-renderer/index.js), FR-VIS-18, FR-VIS-14/15 |
| 22 | `/challenge-funnel [segment]` | Generates a complete Challenge Funnel Brief (FR51): resolves 5 or 7-day duration from tribe's modal Coping Position, validates $9 commitment price through the Commitment Device Gate, binds Hero/Enemy nouns from Character Lexicon. | FR51 (full pipeline), FR-CBCS-04 (ICT Mode), FR0C (Lexicon), → Output: DEP-ENG-072 |
| 23 | `/dm-script [user] [objective]` | Generates a personalized DM script calibrated to the user's SPT stage (vulnerability depth), Coping Position, and Context Premise entities. Uses R-P-V (Recognition → Pivot → Vulnerability) architecture. Runs Dormancy Recovery Gate check before dispatch. | FR-CBCS-02, FR53, FR29 (Neo4j), persuasion_layers.yaml, ttt_matrix.yaml |
| 24 | `/cmf-trivela [user]` | Takes a participant's best drill recording (highest FR61 composite) and processes it through the CMF Trivela Auto-Renderer: branded carousel (Skia), audiogram (CMF pipeline), short-form video caption (Voice DNA styled). The participant walks out with a usable content asset. | FR61, FR-VIS-18 (Skia carousel), FR-VID-13 (audiogram), FR3 (Voice DNA caption) |

### 5.5 Tier 5: Architect Commands (4) — Passphrase-Gated

These commands trigger significant infrastructure changes. Restricted to the platform architect. Two-step passphrase confirmation required (hashed environment variable).

| # | Command | Function | Pipeline Integration |
|---|---|---|---|
| 25 | `/deploy-program [program_id]` | Deploys a new CBCS program instance from the Playbook Library. Provisions Stripe links, Telegram groups, Atlas roadmaps, and accountability partner pairings. | §6.3 Playbooks, FR32, Epic 8.1 (Stripe), FR49 (ADR-01 tenant isolation) |
| 26 | `/swap-drill [day] [new_drill_id]` | Hot-swaps a specific day's drill in the active program without disrupting participant progress. The Board of Learning Optimization Agents is notified. | FR32 (Supabase), §6.4 Board, §6.5 Swarm Intelligence |
| 27 | `/curriculum-refresh [program_id]` | Triggers the Board of Learning Optimization Agents (Atlas + Aria + Assembler) to re-evaluate program structure based on aggregate completion, conviction deltas, and Swarm patterns. Outputs a recommended revision with statistical justification. | FR32, FR-CBCS-09, FR29, FR61, §6.5 Swarm, FR3.1 (Assembler) |
| 28 | `/export-intelligence [scope]` | Exports a full intelligence package for a specified scope (user, segment, cohort, or program). Includes: Voice DNA (FR3/FR61), Context Premise graph (Neo4j), Change Talk Vault (FR-CBCS-01), ICT trajectory (FR-CBCS-04), SPT depth (FR-CBCS-02), TII composite (FR-CBCS-07), SEARCH phase history (FR-CBCS-06). When a coach graduates Law 28 and activates their own CCP, this seeds their container with accumulated intelligence. Their CCP starts smart, not cold. | FR3, FR61, FR29, FR-CBCS-01 through FR-CBCS-07, Neo4j, DEP-ENG-041 |

### 5.6 CPSC / Skia Pipeline Alignment Note

> **⚠️ CRITICAL UPDATE:** The CPSC (Conscious Pose Social Campaign) architecture must be updated to reflect the current Skia rendering pipeline. The original CPSC spec was written before the migration to Skia-based rendering. The following must be reconciled:
> - All promotional flyer generation (`/flyer` command output) must route through the Skia renderer (`src/skia-renderer/index.js`), NOT the legacy image pipeline.
> - The CPSC visual templates must be converted to Skia-compatible JSON scene definitions.
> - The ConsciousPose body language library (FR-VIS-15) and ConsciousSmile expression adapter (FR-VIS-14) must output Skia-compatible overlays.
> - The First Frame Composer (FR-VIS-16) must be validated against the current Skia rendering constraints.
> - A separate CPSC → Skia Migration Brief should be authored to formalize this transition.

### 5.7 Passphrase Protocol

Architect commands (Tier 5) require a two-step confirmation:
1. The architect sends the command (e.g., `/deploy-program law28-cohort-3`)
2. The system responds: `⚠️ This action will provision a new program instance. Confirm with passphrase.`
3. The architect sends the passphrase (stored as a hashed environment variable, never in code).
4. The system executes.

This prevents accidental program-level changes from a mistyped command.

### 5.8 The 28-Command Security Model

| Tier | Auth Level | Commands | Count |
|---|---|---|---|
| 1 — Participant | Public (enrolled user) | `/01` – `/06` | 6 |
| 2 — Coach Ops | Coach-authenticated (JWT + `user_role: coach`) | `/07` – `/12` | 6 |
| 3 — Sales Intel | Coach-authenticated | `/13` – `/20` | 8 |
| 4 — Asset Production | Coach-authenticated | `/21` – `/24` | 4 |
| 5 — Architect | Passphrase-gated (2-step, hashed env var) | `/25` – `/28` | 4 |
| **Total** | | | **28** |

All Coach and Architect commands enforce **ADR-01 Isolation** — queries are scoped to `coach_id = auth.uid()`. No cross-tenant data leakage is possible.

---

## 6. Suggestions & Additions (Architect's Notes)

### 6.1 The "Before/After" Artifact (The Powerful Demonstration)

At Day 1 and Day 28, the system should automatically capture a "Benchmark Recording" — a specific, standardized 2-minute prompt that the participant records at the beginning and end of the program. The FR61 engine generates a side-by-side comparison: Conviction Density (Day 1 vs. Day 28), Hedge Frequency (Day 1 vs. Day 28), Pause Architecture (Day 1 vs. Day 28). This artifact becomes the single most shareable piece of marketing collateral the program produces. It is the "Otis Elevator Demonstration" — the visible, undeniable proof that the transformation is real.

### 6.2 OCR-Based Proof of Work for Non-Voice Programs

For coaches who deploy CBCS programs outside of voice training (e.g., fitness, nutrition, journaling), the "Evidence" capture must support image uploads. The participant photographs their journal entry, their meal, or their workout log. The backend OCR engine (Tesseract or Cloud Vision API) extracts structured data from the image and feeds it to Aria for Context Premise updates. This preserves the "Self-Coding" paradigm for non-audio programs: the act of photographing the evidence IS the proof of change.

### 6.3 The Playbook Library (Master Templates)

We should pre-build 3–5 "Master Playbooks" that coaches can deploy with a single `/deploy-program` command:

| Playbook | Template | Duration |
|---|---|---|
| **Law 28 (Voice Crucible)** | The 5-Pillar Voice Architecture described in this document | 28 days |
| **The Reset Protocol** | A recovery-focused CBCS program for burnout/anxiety (high-compassion TTT) | 30 days |
| **The Revenue Sprint** | A sales-focused CBCS program built on The Challenger methodology | 21 days |
| **The Habit Forge** | A general-purpose behavioral change program (the "vanilla" CBCS) | 30 days |
| **The Couples Protocol** | A relationship-focused CBCS program with dual-participant pairing | 28 days |

Each Playbook includes pre-configured Atlas roadmaps, pre-written drill prompts, pre-set TTT progressions, and pre-tagged Pantry components. The coach adds their own content, their own voice, and their own niche language. The 20% effort (us building the Playbook) produces the 80% outcome (the coach clicking Deploy).

### 6.4 The Board of Learning Optimization Agents

This sub-team within the CBCS Assembler is responsible for continuous program improvement. It consists of:

- **Atlas (Program Architect):** Reviews completion rates, drop-off points, and conviction deltas across all cohorts.
- **Aria (Context Premise Synthesizer):** Analyzes aggregate voice note data to identify the most common fears, breakthroughs, and resistance patterns.
- **The Assembler (Strategist):** Recommends drill modifications based on persuasion layer effectiveness (e.g., "Cohort 3 responded 40% better to Throw Rocks at Enemies than to The Challenger — consider swapping Day 9").

This Board runs a weekly review cycle (aligned with Azaria's Sunday Bot Meeting) and outputs a program revision recommendation. The architect reviews and approves via `/curriculum-refresh`.

### 6.5 Swarm Intelligence Integration

Because all Law 28 participants operate on the same centralized CBCS infrastructure, we have "God-mode visibility" into the aggregate behavioral data. The Swarm Intelligence architecture (promoted from BACKLOG in the MCDA revision) must be instrumented from Day 1:

- **Observation:** Every FR61 score, every Aria extraction, every completion signal is logged.
- **Orientation:** The Board of Learning Optimization Agents runs weekly pattern detection.
- **Decision:** If a specific drill prompt produces a statistically significant conviction gain (>15% above mean), it is flagged as a "Superpower Pattern."
- **Action:** The `/promote-insight` command pushes the pattern to the global AI prompt matrix. All future cohorts benefit from the insight automatically.

This is the Ohio sleep coach example from the MCDA: one participant's breakthrough becomes everyone's upgrade.

---

## 7. Summary: The Law 28 Architecture in Five Pillars

**Pillar 1 — The CBCS Foundation:** Law 28 is a CBCS program instance using the existing 4-Engine architecture (Noise Detector → Neuro-Persuasion → Rapport Interface → Master Composer) to engineer a measurable identity shift from "Timid Content Creator" to "Sovereign Communicator." Every interaction produces richer structured data than any onboarding questionnaire ever could — 28 voice recordings, 28 transcripts, 28 biometric snapshots, hundreds of Context Premise entity extractions.

**Pillar 2 — The Three-Layer Context Premise Architecture:** Coach data from Law 28 feeds **our** Conscious Elite marketing intelligence (Layer 1). Client data from coach-run programs feeds **the coach's** CCP container (Layer 2). Voice DNA universally enriches whichever container owns the relationship (Layer 3). The routing matrix is enforced at the API middleware level via `user_role` and `program_owner_id`.

**Pillar 3 — The 28-Command Intelligence Suite:** The definitive command layer is organized into 5 tiers (6 Participant + 6 Coach Ops + 8 Sales Intel + 4 Asset Production + 4 Architect = **28 commands**). Every command maps to specific CCP data stores and pipeline modules — querying Neo4j Context Premise, FR61 biometrics, Change Talk Vault (FR-CBCS-01), ICT Mapper (FR-CBCS-04), SPT Gauge (FR-CBCS-02), TII (FR-CBCS-07), and SEARCH Phase (FR-CBCS-06). The Sales Intelligence tier (`/segment`, `/webinar-brief`, `/conversion-pulse`, `/offer-check`, `/social-proof`) and Asset Production tier (`/flyer`, `/challenge-funnel`, `/dm-script`, `/cmf-trivela`) transform accumulated program data into on-demand strategic weapons — hyper-targeted scripts, invite lists, Skia-rendered promotional assets, and psychologically matched testimonials built from the exact language the audience uses to describe their own pain.

**Pillar 4 — The CPSC Sales Pipeline Integration:** Commands `/13`–`/20` directly activate the CPSC sales intelligence modules (FR51 Challenge Funnel, FR52 Webinar Brief, FR53 Conversion Sequence, FR54 Promotional Asset, FR55 Session Booking, FR56 Campaign Performance, FR57 Social Proof, FR58 Offer Tier, FR59 Campaign Orchestration, FR60 Loom Report). Every commercial touchpoint is gated by genuine psychological readiness metrics — no arbitrary timers, no manufactured urgency.

**Pillar 5 — The Asymmetric Data Moat:** After 28 days, the CCP knows every participant's Voice DNA profile, Context Premise graph (fears, enemies, dreams, coping mechanisms), Change Talk Vault entries (DARN-CAT commitment language), ICT trajectory, SPT depth, TII bond strength, and SEARCH phase history. The coach types `/segment fear:pricing AND coping:>=3` and within seconds has a list of every person psychologically ready to hear about pricing mastery — along with the exact words each person used to describe their pricing anxiety. No competitor accumulates this data. No competitor can replicate this moat.

---

**END OF BRIEF — DRAFT 3**

*Completed in this revision: Definitive 28-command intelligence suite with full CCP/CBCS/CPSC pipeline integration mapping.*

*Pending: CPSC → Skia Migration Brief, Level 2–12 detailed curriculum, Stripe split-payment integration, final MCDA score update, Conscious Elite marketing Context Premise schema definition, and 28-command backend handler implementation.*
