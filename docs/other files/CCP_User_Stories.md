# CCP User Stories

**Version:** 1.0  
**Derived from:** [CCP_Unified_PRD.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/prd/CCP_Unified_PRD.md) (FR1–FR34)  
**Architecture:** [CCP_Technical_Architecture.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/CCP_Technical_Architecture.md)

**Story Format:** Each story uses the `As a [role], I want [action], so that [value]` pattern with numbered acceptance criteria. Stories are grouped under Epics that map directly to the FR sections in the PRD.

**Roles:**
- **Coach** — The coaching professional (e.g. Nadia). Reviews, publishes, coaches.
- **Client** — The coach's end user (e.g. Amara). Interacts via Telegram only.
- **Audience** — A potential future client (e.g. Kévin). Consumes public content.
- **Operator** — The system administrator (e.g. Mitano). Builds, monitors, maintains.

**Priority:** P0 = launch blocker, P1 = high value, P2 = important but deferrable, P3 = nice-to-have.

---

## Epic 1: Emotional DNA Onboarding (The Trigger-First Pipeline)

*The coach is onboarded not by asking what they believe, but by mathematically mapping what they cannot stop responding to. FR1–FR4.*

### Story 1.1 — Sacred Audio Benchmark & Local Whisper Ingestion

**As an** Operator, **I want** the system to ingest the coach's historical voice notes natively via Telegram and transcribe them locally using Whisper (without external API calls), **so that** we have a private, secure, and highly accurate baseline of their emotional trigger architecture before generating any content.

**Priority:** P0  
**Source:** FR2, Trigger-First Engine Part 3 (Stage 1)

**Acceptance Criteria:**
1. Operator or Coach uploads 10+ minutes of historical "Sacred Audio" (voice notes where the coach is naturally speaking, unscripted) via Telegram.
2. A Local Whisper Pipeline transcribes the audio, ensuring zero external upload for privacy and security.
3. The transcription output is NOT segmented by token limits or paragraphs, but segmented strictly at "complete thought boundaries" (Voice DNA Framework Step 1), preserving full reasoning arcs.
4. The Pipeline evaluates the segmented transcript against Moral Foundations Theory (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression).
5. The extraction outputs the 2 highest-weighted Moral Foundations to `coach_soul.json` under `emotional_dna`.

---

### Story 1.2 — Intelligence as Trigger Fuel

**As the** Genesis System, **I want** to scan weekly intelligence feeds strictly for events that mathematically violate the coach's top 2 Moral Foundations, **so that** I am not presenting "trending topics" but guaranteed "activation events."

**Priority:** P0  
**Source:** Trigger-First Engine Part 3 (Stage 2)

**Acceptance Criteria:**
1. The `Data_Analyst` agent ingests the Tier 1 Context/News feeds.
2. The agent runs a contrastive search against the coach's `emotional_dna.moral_foundations` object.
3. The agent outputs a JSON array of `activation_candidates` containing specific names, clauses, and regulatory mechanics that violate the foundations.
4. Topics that are merely "trending" but have no moral violation overlap are deterministically rejected.

---

### Story 1.3 — DARN-CAT Activation Event Dispatch (Telegram)

**As a** Coach, **I want** to receive a Telegram message detailing a highly specific structural mechanism (not a generic question) and asking for a related episodic memory, **so that** my authentic (autonoetic) memory is triggered rather than my professional mask.

**Priority:** P0  
**Source:** Trigger-First Engine Part 3 (Stage 3)

**Acceptance Criteria:**
1. `The_Interviewer` agent formats a Telegram dispatch based on an `activation_candidate`.
2. The prompt MUST follow the OARS (Open, Affirmation, Reflection, Summarizing) protocol and the DARN-CAT framework.
3. The prompt MUST NOT ask: "What do you think about [X]?" It must ask: "What did you feel the first time you saw [highly specific mechanism] happen?" (Appreciative Inquiry episodic targeting).
4. The system state transitions to `STATE_WAITING_FOR_VOICE`.

---

### Story 1.4 — Authentic Reaction Capture & LIWC-22 Gate

**As the** Genesis System, **I want** to score the coach's resulting voice note segments using the 7 LIWC-22 Authenticity markers, **so that** only genuinely activated material enters the generation pipeline and performed material is blocked.

**Priority:** P0  
**Source:** FR2, Trigger-First Engine Part 3 (Stage 4)

**Acceptance Criteria:**
1. The coach replies with a voice note via Telegram in response to a DARN-CAT trigger.
2. The Local Whisper Pipeline transcribes and segments the response into logical Thought Units.
3. The system parses each transcript segment and scores it against 7 LIWC-22 markers:
   - 1st-person singular frequency
   - Exclusive word count (e.g., *but*, *except*)
   - Absence of hedging language
   - Sentence compression (words per sentence ratio)
   - Verb tense distribution (present tense vs past tense)
   - Filler frequency (e.g., *um*, *uh*)
   - Discourse marker position
4. A composite `Authenticity_Score` (0.0 to 1.0) is calculated for each segment based on the 7 markers.
5. If the segment's composite score evaluates to `< 0.60`, it is flagged and discarded, and the system automatically replies with a revised Activation Event to re-attempt episodic extraction.
6. If the composite score is `>= 0.60`, the segment is saved to the `Authentic_Material_Payload`.

---

### Story 1.5 — Emotional State to Archetype Routing

**As the** Genesis System, **I want** to select the specific post format (Archetype) based exclusively on the emotional vector detected in the voice note, **so that** the archetype serves the emotion, not the topic.

**Priority:** P1  
**Source:** Trigger-First Engine Part 3 (Stage 5)

**Acceptance Criteria:**
1. The routing matrix evaluates the dominant emotional vector of the `Authentic_Material_Payload`.
2. "Disgust + Protective Fury" strictly maps to `myth_indignation` or `reaction_outrage`. "Outrage at Opacity" maps to `listicle_shocking`, etc.
3. The selected archetype checks the coach's `Voice_DNA.TTT_Ceiling` to ensure the coach can credibly occupy the required Temperature of the archetype.
4. The final `DEP-LIB-009` Design Brief Template is injected into the payload.

---

### Story 1.6 — Generation & Powerless Observer Override

**As the** Genesis System, **I want** to execute the Prompt Assembly while specifically overriding the LLM's default highly agreeable tone, **so that** the final content hits the exact anger, validation, or precision the coach originally felt.

**Priority:** P0  
**Source:** Trigger-First Engine Part 3 (Stage 7)

**Acceptance Criteria:**
1. The Generation Agent receives the full payload.
2. An SPR (System Prompt Re-engineering) block is injected explicitly forbidding the "Powerless Observer Bias" (the LLM's tendency to soften hard stances).
3. The generated content is parsed to ensure it mirrors the exact syntactic markers recorded in Stage 4.
4. The final piece is written to Supabase `content_performance_db` with its `trigger_activation_code` and `LIWC_authenticity_score` appended.

---

### Story 1.7 — Mandate 4: Negative Space Excavation First

**As the** Genesis System, **I want** to build the Negative Space Object (`DEP-ENG-004`) before analyzing any positive traits, **so that** the downstream generators are constrained by strict boundaries (Mandate 4) preventing LLM hallucination and generic "coach-speak."

**Priority:** P0  
**Source:** FR3, Mandate 4, Voice DNA Framework (Step 7)

**Acceptance Criteria:**
1. The `voice-dna-profiler/` skill consumes the validated `Authentic_Material_Payload`.
2. The agent executes Step 7 (Negative Space Excavation) explicitly before running the 60-variable stylometry analysis.
3. The agent identifies Lexical Blacklists, Syntactic Impossibilities, and Structural Exclusions from the coach's transcripts.
4. The output is saved to `coach_soul.json` as `DEP-ENG-004` and locked as an unalterable constraint for all subsequent generation steps.

---

### Story 1.8 — 3D Voice DNA Registration & Cross-Topic Validation

**As the** Genesis System, **I want** to extract the coach's 60-variable stylometry profile and verify it across 5 distinct topics, **so that** the Positive Space Object (`DEP-ENG-003`) reflects structural habits rather than topic-specific vocabulary.

**Priority:** P0  
**Source:** FR3, Voice DNA Framework (Steps 2, 3, 4)

**Acceptance Criteria:**
1. The system performs Step 2 (Discourse Marker Census) and Step 3 (Sentence Skeleton Extraction) to map the coach's Function Word Adjacency Networks (WAN).
2. The 60-variable computational stylometry profile is extracted covering: Lexical, Syntactic, Relational, Graphical, and Complexity clusters.
3. Step 4 triggers: The profile is run against transcripts of the coach speaking on 5 maximally different subjects.
4. Only formatting and structural rules invariant across all 5 subjects are committed to the `DEP-ENG-003` (Positive Space Object) in `coach_soul.json`.

---

### Story 1.9 — Adversarial Generation Validation

**As an** Operator, **I want** the system to stress-test the synthesized Voice DNA by autonomously attacking its own outputs, **so that** any trace of "imposter" phrasing is eliminated before the profile is finalized.

**Priority:** P0  
**Source:** FR3, Voice DNA Framework (Step 12)

**Acceptance Criteria:**
1. Once `DEP-ENG-003`, `DEP-ENG-004`, and `DEP-LIB-001` are populated, the generator produces 5 unique content outputs using the new DNA.
2. The Adversarial Validator agent attacks these 5 outputs specifically looking for identity drift, "generic AI" smoothing, or violations of the Negative Space.
3. If any output is successfully flagged for inauthenticity, the system logs the failure reason, rewinds to refine the Negative Space (Step 7), and loops back.
4. If all 5 outputs survive the attack, `coach_soul.json v3.1` is finalized and sealed for production use.

---

## Epic 2: Real-Time Coaching Intelligence (CBCS)

*The client receives daily coaching interactions via Telegram that feel deeply personal. FR5–FR9.*

### Story 2.1 — Daily Accountability Rituals

**As a** Client, **I want** to receive a daily accountability message via Telegram that references my specific situation, **so that** I stay on track without feeling like I'm talking to a bot.

**Priority:** P0  
**Source:** FR5

**Acceptance Criteria:**
1. Daily ritual message is delivered within the coach-configured time window (e.g. 7:00–7:30 AM).
2. Message references specific details from the client's Context Premise (e.g., the boundary they're working on, the fear they named).
3. Client can respond via voice note or text. Both are processed.
4. Response is parsed by Aria (Context Analyst) and updates the client's Context Premise graph.
5. Message tone matches the coach's Voice DNA via TTT calibration (drift < 15%).
6. If the client doesn't respond within 24 hours, a different-toned follow-up is sent (not a repeat).

---

### Story 2.2 — Personalized Journaling Prompts

**As a** Client, **I want** to receive journaling prompts 2–3 times per week that evolve with my progress, **so that** my reflections stay meaningful rather than repetitive.

**Priority:** P1  
**Source:** FR6

**Acceptance Criteria:**
1. Journaling prompts are drawn from the client's current emotional arc and recent interactions.
2. Prompts reference specific moments from previous responses (not generic templates).
3. Boredom Ban constraint applies: no prompt archetype (e.g. "describe a moment when...") repeats within 3 weeks.
4. Client's journal responses are stored, transcribed (if voice), and added to the Context Premise map.
5. Prompts are scheduled at coach-configured intervals (e.g. Mon/Wed/Fri evenings).

---

### Story 2.3 — Voice Note Context Extraction

**As a** Coach, **I want** the system to parse my clients' unstructured voice notes and automatically update their psychological profiles, **so that** I always have current insight without manually reviewing every message.

**Priority:** P0  
**Source:** FR7

**Acceptance Criteria:**
1. Groq transcription completes within 5 seconds of voice note receipt.
2. Aria extracts and updates Context Premise dimensions: Fears, Enemies, Dreams, Allies, Victories, Patterns.
3. Significant new patterns trigger a Notion comment on the client's page (pattern alert).
4. Extraction runs within the end-to-end < 2 second CBCS response window (P95).
5. All extractions are logged in the Receipt Chain with the source message reference.

---

### Story 2.4 — Dormancy Recovery

**As a** Coach, **I want** the system to automatically re-engage clients who go silent, **so that** I don't lose clients to simple inattention.

**Priority:** P1  
**Source:** FR8

**Acceptance Criteria:**
1. System detects silence after a configurable threshold (default: 72 hours without interaction).
2. First recovery attempt uses a different emotional angle than the client's last interaction (not a repeat of the last message type).
3. Recovery messages are coach-voiced (TTT calibrated) — not system notifications.
4. Escalation ladder: Day 3 → gentle nudge, Day 5 → callback to a past victory, Day 7 → direct question, Day 10 → Coach is notified via Telegram with context.
5. Client's response after dormancy triggers a "welcome back" flow, not a guilt trip.

---

### Story 2.5 — Crisis Detection & Circuit Breaker

**As a** Coach, **I want** the system to detect crisis signals in my clients' messages and immediately stop automated responses, **so that** no AI message makes a distressed client feel worse.

**Priority:** P0  
**Source:** FR9

**Acceptance Criteria:**
1. Crisis keyword detection runs on every incoming message (first-pass, before any other processing).
2. Trigger words/patterns include: self-harm indicators, severe distress language, suicidal ideation markers (configurable list).
3. On trigger: all automated responses halt immediately for this client.
4. Coach receives a Telegram notification within 10 seconds with the flagged message and client context.
5. System logs the Circuit Breaker activation in the Receipt Chain.
6. Automated interactions resume only when the Coach explicitly resets the Circuit Breaker.

---

## Epic 3: Content Production Engine (CCF)

*36 content pieces per week, across 14 formats, in the coach's voice. FR10–FR16.*

### Story 3.1 — Weekly Content Pipeline Trigger

**As an** Operator, **I want** to trigger the weekly content pipeline with a single command, **so that** 36 content pieces are produced autonomously through the full research → generate → validate cycle.

**Priority:** P0  
**Source:** FR10

**Acceptance Criteria:**
1. `ccf-weekly` triggers the 19-command pipeline in sequence.
2. Pipeline starts with research and guided questioning (Stream of Consciousness capture), never raw generation.
3. The 3 Embedded Governance Ministers (Identity, Relevance, Timing) run inline during generation.
4. The Validation Team (Sophia → Marcus → Chen) triple-pass gate runs on every piece.
5. Failed pieces enter a TillDone rewrite loop (max 3 attempts before Operator flag).
6. Full pipeline completes within the configured time window (target: < 45 minutes for 36 pieces).
7. Receipt Chain logs every step with source traceability.

---

### Story 3.2 — Coach Topic Suggestions

**As a** Coach, **I want** to suggest topics for future content via Telegram, **so that** my content reflects what's on my mind without me having to write anything.

**Priority:** P1  
**Source:** FR10a

**Acceptance Criteria:**
1. Coach sends a voice note or text message with a topic idea to the Telegram bot.
2. Suggested topics are transcribed, tagged, and added to the topic queue.
3. Topics enter the standard research pipeline before generation (no raw generation from suggestions).
4. The system acknowledges the suggestion and indicates when it will be incorporated (next batch or future).
5. Topic suggestions carry a `SUGG` Asset ID for traceability.

---

### Story 3.3 — Content Cadence Limits

**As an** Operator, **I want** the system to enforce monthly content generation limits per coach, **so that** no coach exceeds their contracted volume.

**Priority:** P2  
**Source:** FR10b

**Acceptance Criteria:**
1. The ContentCadence Extension tracks monthly production count per coach.
2. When the limit is reached, `ccf-weekly` auto-pauses and the Operator is notified.
3. Limit is configurable per coach in the coach profile.
4. Partial batches are not generated — the system warns before starting if the remaining quota is insufficient for a full batch.

---

### Story 3.4 — Multi-Format Content Generation

**As a** Coach, **I want** the system to produce content across 14 formats from a single pipeline run, **so that** I have a complete content library without format-specific effort.

**Priority:** P0  
**Source:** FR11

**Acceptance Criteria:**
1. Output includes all 14 formats: threads, carousels, reels scripts, static image quotes, meme concepts, stories, polls, long-form articles, case studies, tips, lists, reaction scripts, tweet storms, and visual explainers.
2. Format assignment is driven by leadership trait scores (weak traits → exercise formats, strong traits → showcase formats).
3. Each piece carries its format-specific Asset ID (e.g. `SCRP`, `VIMG`, `QUOT`, `MEME`).
4. All formats share the same Voice DNA (TTT consistency across formats).

---

### Story 3.5 — Voice DNA Enforcement

**As a** Coach, **I want** every piece of content to sound like me, **so that** my audience never suspects the content is AI-assisted.

**Priority:** P0  
**Source:** FR12

**Acceptance Criteria:**
1. TTT alignment check runs on every generated piece before validation.
2. Drift threshold: < 15%. Pieces exceeding threshold are flagged for rewrite.
3. Chen (Soul Validator) performs the final voice consistency check.
4. Metrics logged: TTT alignment score, flagged drift dimensions (vocabulary, rhythm, tone, metaphor).
5. Progressive calibration: Voice DNA updates weekly from coach feedback on approved content.

---

### Story 3.6 — Strategic Humor Integration

**As a** Coach, **I want** humor (tweets + memes) to be woven into every content batch naturally, **so that** my content mix feels human and diverse, not all-serious.

**Priority:** P1  
**Source:** FR13, FR13a, FR13b

**Acceptance Criteria:**
1. Every batch includes at least 2 humor pieces (tweets, memes, or humor-angle scripts).
2. The Humor Agent proposes setups, plot twists, ironic/absurd/awkwardly relatable angles.
3. Humor passes the Vibe Check — no generic AI humor (puns, dad jokes, corporate funny).
4. The Tweet Meteorologist Agent forecasts digital conversation weather (sentiment climate, viral trends, meme explosions) and informs timely angles.
5. Humor tone is calibrated to the coach's humor style (extracted during onboarding).

---

### Story 3.7 — Boredom Ban Enforcement

**As a** Coach, **I want** the system to guarantee no thematic repetition over 8 weeks, **so that** my audience never feels like they're seeing the same content recycled.

**Priority:** P0  
**Source:** FR14

**Acceptance Criteria:**
1. An 8-week rolling window tracks all published themes, angles, metaphors, and story structures.
2. New content is checked against the window before validation.
3. Matches trigger a redirect to the generation phase with explicit "avoid X" constraints.
4. The window is per-coach, per-format — a metaphor used in a thread CAN be used in a reel, but not in another thread.
5. Window data is stored in Episodic Memory and queryable by the Operator.

---

### Story 3.8 — Operator Content Review & Approval

**As an** Operator, **I want** to review, edit, and approve all generated content before it reaches the coach, **so that** only production-quality content is delivered.

**Priority:** P0  
**Source:** FR15

**Acceptance Criteria:**
1. All Validation Team-passed content enters an Operator review queue.
2. Operator can approve, reject (with reason), or edit each piece.
3. Edits preserve the Receipt Chain entry — both original and edited versions are logged.
4. Rejected pieces re-enter the TillDone loop with the rejection reason as generation context.
5. Approved content is pushed to the coach's Notion Content Calendar via `notion_sync.py`.

---

### Story 3.9 — Manual Publishing (Vibe-Baiting)

**As a** Coach, **I want** to publish approved content manually to my social media, **so that** publishing remains my personal touchpoint with my audience.

**Priority:** P0  
**Source:** FR16

**Acceptance Criteria:**
1. Approved content in Notion includes all assets needed for publishing: script text, visual files, posting notes (platform-specific instructions), and recommended posting time.
2. The system NEVER auto-publishes. Publishing is always a manual coach action.
3. Posting Notes include hashtag suggestions, caption variants, and engagement prompts per platform.
4. After the coach publishes, engagement data flows back into the feedback loop (Sunday Bot Meeting).

---

## Epic 4: Webinar & Visual Asset Automation (V2WS & Tierlist)

*Webinar scripts + visual slides delivered as coach-ready Excalidraw files. FR17–FR20.*

### Story 4.1 — YOLO Mode Webinar Creation

**As a** Coach, **I want** to answer 5 questions and receive a complete branded webinar package, **so that** I can prepare a full webinar in hours instead of weeks.

**Priority:** P1  
**Source:** FR17 (YOLO Mode), FR17a

**Acceptance Criteria:**
1. Coach answers 5 focused questions: (1) what to teach, (2) who the audience is, (3) what the offer is, (4) key stories/examples, (5) tone/energy level.
2. System runs DEEP/FRESH research before generating any module.
3. Output: a branded `.excalidraw` file with module scripts embedded as text layers.
4. Each slide is engineered as a HOOK, not a presentation slide.
5. Webinar passes the 4 Distillation stages and Boredom Ban.
6. Asset ID: `WBNR-CCC-MM-YY-XXXX` for the package, `WSLD-CCC-MM-YY-XXXX` per slide.
7. Coach can export to PDF/PPTX natively from Excalidraw if needed.

---

### Story 4.2 — Interactive Mode Webinar Creation

**As a** Coach, **I want** to collaboratively build a webinar module-by-module via Telegram, **so that** I can shape the content as it's being created.

**Priority:** P2  
**Source:** FR17 (Interactive Mode), FR17a

**Acceptance Criteria:**
1. Session starts with Stream of Consciousness capture — the coach describes what they want to teach.
2. System writes one module at a time and presents it via Telegram for approval.
3. Coach can approve, request changes, or redirect each module.
4. Agent has full access to Intelligence Library and Memory for context-aware suggestions.
5. Coach can upload image assets at any point. System incorporates them into the final Excalidraw file.
6. Output: the same branded `.excalidraw` package as YOLO mode.

---

### Story 4.3 — Dynamic Module Adjustment

**As an** Operator, **I want** the system to adjust webinar module selection based on aggregate audience data, **so that** webinars emphasize what matters most to the current audience.

**Priority:** P2  
**Source:** FR18

**Acceptance Criteria:**
1. Audience Context Premises are aggregated to identify dominant themes (fears, dreams, patterns).
2. Module ranking adjusts based on theme relevance to the current audience composition.
3. Adjustment is logged in the Receipt Chain with the reasoning.
4. Coach is informed of the adjustment rationale (not just the result).

---

### Story 4.4 — Unified Excalidraw Visual Pipeline

**As an** Operator, **I want** all visual long-form content to use a single Excalidraw pipeline, **so that** Tierlists, Ratings, Webinar slides, and Reaction Explainers share the same process and aesthetic.

**Priority:** P1  
**Source:** FR19, FR19a

**Acceptance Criteria:**
1. Same branded Excalidraw templates are used across all visual content types.
2. The Transparent Collage Pipeline for stick figures runs for emotionally-aware illustrations: Visual Reasoning Protocol → T2I prompt (white background) → alpha extraction → transparent PNG injection into `.excalidraw` JSON.
3. Each visual asset carries the appropriate Asset ID (`TIER`, `RTNG`, `WSLD`, `REXP`).
4. No static illustration library — every stick figure is generated in context.
5. Output files are functional `.excalidraw` files the coach can open and record over.

---

### Story 4.5 — Images Over Videos for Reaction Content

**As a** Coach, **I want** reaction-style content to use curated images instead of video clips, **so that** I remain the sole video presence and avoid sourcing/licensing issues.

**Priority:** P1  
**Source:** FR20

**Acceptance Criteria:**
1. Reaction Explainer slides contain only static images — no embedded video.
2. Images are sourced, classified, and arranged to maintain the coach's attention flow.
3. The coach IS the video — they record themselves reacting to the visual frames.
4. Image assets carry the `RIMG` Asset ID.

---

## Epic 5: Cross-System Intelligence & Memory

*Data flows between CCF, CBCS, and back — making everything smarter over time. FR21–FR24a.*

### Story 5.1 — Client Context Premise Graph

**As a** Coach, **I want** each client's psychological profile stored as an interconnected graph, **so that** coaching interactions draw on the full picture of a client, not isolated data points.

**Priority:** P0  
**Source:** FR21

**Acceptance Criteria:**
1. Each client's Context Premise is stored in Neo4j with nodes for Fears, Enemies, Dreams, Allies, Victories, and Patterns.
2. Relationships connect related dimensions (e.g., a Fear linked to a triggering Enemy, a Victory that overcame a Fear).
3. Graph is updated in real-time from CBCS interactions (voice notes, journal entries, ritual responses).
4. Client page in Notion surfaces the profile as a clean narrative (no graph terminology).
5. Data isolation: each coach has a dedicated graph schema. Zero cross-pollination.

---

### Story 5.2 — CBCS-to-CCF Intelligence Loop

**As an** Operator, **I want** aggregate client interaction data to inform the next content production cycle, **so that** content evolves toward what actually helps clients.

**Priority:** P1  
**Source:** FR22

**Acceptance Criteria:**
1. Sunday Bot Meeting aggregates patterns across all of a coach's clients: dominant fears, breakthrough themes, friction points.
2. Aggregated signals are available to `ccf-analyze` during the next weekly pipeline run.
3. No individual client data is exposed in content — only aggregate patterns.
4. Intelligence flow is logged in the Receipt Chain.

---

### Story 5.3 — Content Performance Feedback Loop

**As an** Operator, **I want** content engagement data from social platforms to feed back into coaching interactions, **so that** clients hear their coach talk about the things the audience resonates with.

**Priority:** P2  
**Source:** FR23

**Acceptance Criteria:**
1. Engagement metrics (saves, shares, comments, DM triggers) are captured per content piece.
2. High-performing content themes are tagged as "resonance markers" in the coach's profile.
3. CBCS rituals can reference high-performing public content ("Your coach just wrote something about exactly this — have you seen it?").
4. Resonance markers influence the next content cycle's theme weighting.

---

### Story 5.4 — Monthly Cross-Ecosystem Meeting

**As an** Operator, **I want** each coach's system to share learnings with other coach ecosystems once per month, **so that** system-wide intelligence improves for all coaches.

**Priority:** P3  
**Source:** FR24

**Acceptance Criteria:**
1. Each ecosystem designates one representative agent for the meeting.
2. Shared data is anonymized — no coach-specific content or client data crosses boundaries.
3. Shared learnings: format performance patterns, engagement trends, dormancy recovery strategies.
4. Meeting output is a summary document available to the Operator.
5. First meeting scheduled: April 1, 2026.

---

### Story 5.5 — Autonomous Memory Promotion

**As an** Operator, **I want** the system to autonomously promote recognized patterns from Working → Episodic → Semantic memory, **so that** the most important learnings become permanent intelligence.

**Priority:** P1  
**Source:** FR24a

**Acceptance Criteria:**
1. Azaria (Memory Curator) evaluates patterns based on frequency, consistency, and impact.
2. Promotion candidates are flagged for Operator review (FR28).
3. Approved promotions move from Episodic → Semantic Memory.
4. Promoted patterns influence all downstream generation and coaching.
5. Rejected promotions are logged with the Operator's reasoning.

---

## Epic 6: System Operations & Governance

*The operator's toolkit for monitoring, tracing, managing, and scaling the platform. FR25–FR29.*

### Story 6.1 — Receipt Chain Monitoring

**As an** Operator, **I want** to view a continuous log of every agent interaction, API call, and validation decision, **so that** I can audit any system behavior.

**Priority:** P0  
**Source:** FR25

**Acceptance Criteria:**
1. Receipt Chain logs are queryable by coach, date range, agent, and operation type.
2. Each entry includes: timestamp, agent ID, action, input hash, output hash, decision rationale.
3. Logs are immutable — no entry can be modified after creation.
4. Logs are accessible via CLI and a log viewer interface.

---

### Story 6.2 — Output Provenance Tracing

**As an** Operator, **I want** to trace any published piece of content back to the exact prompt, context window, and decision tree that produced it, **so that** I can debug quality issues to the root cause.

**Priority:** P0  
**Source:** FR26

**Acceptance Criteria:**
1. Given any Asset ID, the system returns the full provenance chain: source data → research → generation prompt → agent output → validation decisions → edits → final version.
2. Context window contents are stored (compressed) for each generation step.
3. Provenance is available within 5 seconds of query.
4. Visualization: chain of custody view showing each transformation step.

---

### Story 6.3 — Agent Roster Management

**As an** Operator, **I want** to update agent prompt strategies, skills, and tools across the ecosystem, **so that** I can evolve the system without redeploying infrastructure.

**Priority:** P1  
**Source:** FR27

**Acceptance Criteria:**
1. Operator can edit any agent's SKILL.md, prompt template, or tool configuration.
2. Changes take effect on the next pipeline run (no restart required).
3. All changes are versioned and logged in the Receipt Chain.
4. Rollback is available to any previous version of an agent's configuration.

---

### Story 6.4 — Memory Promotion Review

**As an** Operator, **I want** to review and approve or reject automated memory promotions, **so that** no false pattern permanently contaminates the system's intelligence.

**Priority:** P1  
**Source:** FR28

**Acceptance Criteria:**
1. Promotion candidates are presented with: the pattern, evidence (source messages/interactions), frequency count, and Azaria's confidence score.
2. Operator can approve, reject with reason, or defer.
3. Rejected patterns are marked "reviewed-rejected" and won't be re-proposed unless new evidence surface.
4. Approved patterns are promoted and take effect in the next cycle.

---

### Story 6.5 — Coach Instance Provisioning

**As an** Operator, **I want** to spin up a new, securely isolated cloud instance for each coach, **so that** every coach's data is completely separate from every other coach.

**Priority:** P0  
**Source:** FR29

**Acceptance Criteria:**
1. Pi Coding Agent provisions a new single-tenant instance with all required services (Neo4j, Supabase schema, Redis namespace, file storage directory).
2. Instance is securely isolated — no shared database connections, no shared file paths.
3. Instance includes pre-configured Notion workspace templates for the 4 databases.
4. NOTION_TOKEN and all credentials are securely stored and scoped to this instance.
5. Provisioning completes within 15 minutes including verification checks.

---

## Epic 7: Notion Delivery Layer & Asset Tracking

*Everything the coach sees happens in Notion. FR30–FR34.*

### Story 7.1 — Autonomous Content Delivery to Notion

**As a** Coach, **I want** all validated content to appear in my Notion Content Calendar automatically, **so that** I never wait for deliveries or check external systems.

**Priority:** P0  
**Source:** FR30, FR30a

**Acceptance Criteria:**
1. `notion_sync.py` pushes content pages to the Content Calendar within 60 seconds of Operator approval.
2. Each content page contains 7 structured sections: 🎙️ Coach Voice Note (audio block), 💡 Why This Post (origin trace to coach's own words), 🌱 Leadership Farming (trait development note), 📄 Script, 📸 Coach Photo (from Branding Deck), 🖼️ Visual Assets, 📋 Posting Notes.
3. Properties are populated: Title, Asset ID, Format, Publish Date, Platform, Status (Draft), Season.
4. Content appears styled — bold + colored backgrounds + callout blocks — not plain text.
5. Zero manual intervention after pipeline approval. Push is fully autonomous.
6. Push failures are retried 3 times with exponential backoff. Persistent failures alert the Operator.

---

### Story 7.2 — Universal Asset ID Assignment

**As an** Operator, **I want** every artifact in the system to carry a unique, human-readable ID, **so that** any asset can be traced across Notion, Supabase, Receipt Chain, and file storage.

**Priority:** P0  
**Source:** FR31

**Acceptance Criteria:**
1. Format: `AAAA-CCC-MM-YY-XXXX` — Asset Type (4 chars), Coach Acronym (3 chars), Month (2 digits), Year (2 digits), Random Suffix (4 alphanumeric).
2. 34 asset type codes are registered across CCF, V2WS, Tierlist, CBCS, Coach Identity, and Governance.
3. IDs are generated at creation time and never change.
4. Zero collisions across 1000 IDs per type/coach/month (verified by uniqueness check).
5. Asset ID is stored as a property on every Notion page and in the Receipt Chain.

---

### Story 7.3 — Person ID System

**As a** Coach, **I want** every client to have a unique ID, **so that** I can reference clients consistently across my workspace.

**Priority:** P1  
**Source:** FR31a

**Acceptance Criteria:**
1. Format: `CCC-NNNN` — Coach Acronym (3 chars) + sequential client number (4 digits).
2. Coach's own ID: `CCC-0000`.
3. Clients are numbered sequentially starting from `CCC-0001`.
4. Person ID is assigned during CBCS onboarding (first message exchange).
5. Person ID is stored in `coach_registry.json` and on the client's Notion page.
6. Person IDs are unique per coach ecosystem. No cross-ecosystem references.

---

### Story 7.4 — Notion Dashboard UX (Conditional Color & Formulas)

**As a** Coach, **I want** my Notion workspace to use color-coding and smart formulas to surface intelligence visually, **so that** I understand my practice's health at a glance without reading everything.

**Priority:** P1  
**Source:** FR32, FR32a

**Acceptance Criteria:**
1. Content Calendar conditional colors: 🔴 overdue, 🟢 on-schedule, 🟡 due tomorrow, 🔵 seasonal match.
2. Client Intelligence conditional colors: 🟢 engaged (streak ≥ 14), 🔴 dormant (silent ≥ 7 days), 🟡 declining sentiment.
3. Smart formulas: countdown pulse (days until publish), emoji progress bars (milestone completion), engagement heat indicator (streak → text label), resonance hit (content–client theme match).
4. Content pages use tabbed layouts: Script / Visuals / Metrics.
5. Client pages use tabbed layouts: Profile / Sessions / Voice Journal.
6. Photo Deck conditional color: overused photos (usage ≥ 4) flagged.

---

### Story 7.5 — Personal Branding Photo Deck

**As a** Coach, **I want** to upload my real photos to Notion for use in quote cards and carousels, **so that** my content features my actual face, not AI-generated imagery.

**Priority:** P1  
**Source:** FR33

**Acceptance Criteria:**
1. Photo Deck database accepts image uploads with metadata: Mood, Setting, Format.
2. Each photo gets a `PHOT-CCC-MM-YY-XXXX` Asset ID.
3. Photos are stored in Supabase Storage and referenced in Notion.
4. Usage Count property tracks how many times each photo has been used.
5. Conditional color flags overused photos (count ≥ 4).
6. **Sovereign Image Rule enforced:** AI-generated coach imagery is blocked system-wide. AI images represent client scenarios only.

---

### Story 7.6 — Webhook-Triggered Distribution

**As a** Coach, **I want** changing a content piece's Status to "Approved" in Notion to trigger the distribution pipeline, **so that** I don't need any external tool or extra step to publish.

**Priority:** P1  
**Source:** FR34

**Acceptance Criteria:**
1. Notion automation detects Status change: Draft → Approved.
2. Automation sends a webhook to the CCP distribution endpoint.
3. The distribution pipeline receives the Asset ID and processes: generate posting-ready files, update Receipt Chain, mark status as "Ready to Post."
4. Coach receives a Notion notification confirming the piece is ready.
5. Webhook failures are retried 3 times. Persistent failures notify the Operator.
6. Only the Approved → Ready transition triggers the webhook (not other status changes).

---

## Story Dependency Map

```
Epic 1 (Genesis) ──────────┐
                           ├──→ Epic 3 (CCF) ──→ Epic 7 (Notion Delivery)
Epic 2 (CBCS) ─────────────┤
                           ├──→ Epic 4 (V2WS/Tierlist)
Epic 5 (Intelligence) ◄────┤
                           │
Epic 6 (Operations) ◄──────┘
```

**Critical path:** Epic 1 → Epic 3 → Epic 7 (coach exists → content produced → delivered to Notion).

---

## Story Count Summary

| Epic | Stories | P0 | P1 | P2 | P3 |
|---|---|---|---|---|---|
| 1. Coach Genesis | 7 | 7 | 0 | 0 | 0 |
| 2. CBCS | 5 | 3 | 2 | 0 | 0 |
| 3. CCF | 9 | 5 | 3 | 1 | 0 |
| 4. V2WS & Tierlist | 5 | 0 | 3 | 2 | 0 |
| 5. Intelligence & Memory | 5 | 1 | 2 | 1 | 1 |
| 6. Operations | 5 | 2 | 2 | 0 | 0 |* 
| 7. Notion Delivery | 6 | 2 | 4 | 0 | 0 |
| **Total** | **42** | **20** | **16** | **4** | **1** |

*Story 6.5 is P0 despite being in the Operations epic because coach provisioning is a launch prerequisite.
