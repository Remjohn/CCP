# Tech-Spec: FR-CA11-22 — Studio Stream Overlay & Trivianar Display

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-22), ADR-07
**Skill Implementation:** `ccp-blocks/studio-block/components/TriviaOverlay.tsx`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-22)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Interactive_Trivianar_Engine.md` (§4b Stream Overlay)

---

## 2. Overview

### Problem Statement
During live streams, the Trivianar Engine runs in Telegram — but viewers watching the stream on YouTube/Facebook see nothing. There is no visual representation of trivia questions, answer distributions, leaderboards, or winner reveals on the stream itself. This disconnects the stream audience from the interactive experience.

### Solution
FR-CA11-22 implements a **React overlay component** (`<TriviaOverlay />`) rendered on the Studio Block's recording canvas during webinar/stream mode. The overlay receives real-time events from the Trivianar Engine via WebSocket and displays: question text with countdown bar, color-coded answer distribution after votes, leaderboard panel sliding in from the right, and winner reveal with confetti animation.

### Scope
**In scope:**
- React overlay component rendered on canvas.
- WebSocket client receiving Trivianar events.
- Question display with countdown timer bar.
- Answer distribution visualization (color-coded bars).
- Leaderboard slide-in panel (top 5 participants).
- Winner reveal animation (3rd→2nd→1st with confetti).
- DPA branding integration (FR-CA11-15 brand colors/fonts).

**Out of scope:**
- Trivianar Engine logic (FR-CA11-19).
- Telegram-side rendering.
- Full-screen audience participation view (this is the stream-side overlay only).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-098` | Overlay React Component | UI — `<TriviaOverlay />` React component with Framer Motion animations. |
| `DEP-ENG-099` | Question Display Module | UI — Question text + countdown bar + answer option labels. |
| `DEP-ENG-100` | Answer Distribution Renderer | UI — Color-coded horizontal bars showing vote distribution per option. |
| `DEP-ENG-101` | Leaderboard Panel | UI — Top-5 participant list sliding in from right side. |
| `DEP-ENG-102` | Winner Reveal Animation | UI — Sequential 3rd→2nd→1st reveal with `canvas-confetti` celebration. |
| FR-CA11-19 | Trivianar Engine | UPSTREAM — Emits WebSocket events: `question_sent`, `answer_distribution`, `leaderboard_updated`, `winner_reveal`. |
| FR-CA11-15 | DPA Branding | UPSTREAM — Provides coach brand colors and fonts for overlay styling. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Dual-Screen Engagement** | Proulx & Shepatin | 2012 | Second-screen experiences (Telegram trivia) combined with first-screen visualization (stream overlay) create deeper engagement than either alone. |
| **Information Visualization** | Tufte | 2001 | Answer distribution bars encode multiple data dimensions (option text, vote count, percentage) in a single glanceable element. |

### Technical Decisions
1. **Canvas Overlay (not DOM):** The overlay is rendered to a separate off-screen `<canvas>`, which is then composited onto the main recording canvas via `drawImage()`. This ensures the overlay appears in the stream/recording output without iframe or DOM layering issues.
2. **Framer Motion for Animations:** Framer Motion drives slide-in, fade, scale, and confetti trigger timing. Animations are rendered to a React tree, then captured to the overlay canvas via `html2canvas` or a custom renderer.
3. **WebSocket Event-Driven:** The overlay is purely reactive — it renders nothing until a Trivianar event arrives. States: `idle` (no overlay), `question` (showing question + countdown), `distribution` (showing answer bars), `leaderboard` (sliding panel), `winner` (confetti reveal).

---

## 4. Implementation Plan

### Stage 1: WebSocket Client & State Machine
*DEP-ID:* `DEP-ENG-098`

**Steps:**
1. Build WebSocket client connecting to Trivianar Engine: `ws://trivianar-engine/overlay/{stream_id}`.
2. Implement state machine: `idle → question → distribution → leaderboard → winner → idle`.
3. State transitions driven by events:
   - `question_sent` → transition to `question` state.
   - `question_closed` + `distribution` payload → transition to `distribution` state.
   - `leaderboard_updated` → transition to `leaderboard` state.
   - `winner_reveal` → transition to `winner` state.
   - `clear` → transition to `idle` state.

### Stage 2: Question Display
*DEP-ID:* `DEP-ENG-099`

**Steps:**
1. Render question text in the lower third of the canvas (standard broadcast lower-third positioning).
2. Background: semi-transparent card (rgba(0,0,0,0.75)) with DPA brand accent border.
3. Countdown bar: horizontal progress bar above question text. Animates from full width to 0 over `time_limit_seconds`.
4. Answer options: 4 labels (A, B, C, D) displayed below question in a 2×2 grid, each with distinct brand-accent color.

### Stage 3: Answer Distribution
*DEP-ID:* `DEP-ENG-100`

**Steps:**
1. After `question_closed` event: animate question text out (fade up).
2. Show 4 horizontal bars, each colored to match the option label color.
3. Bar width proportional to vote percentage. Bars animate from 0 to final width over 1 second.
4. Correct answer bar highlighted with a glow effect (box-shadow pulse animation).
5. Display vote count and percentage next to each bar.

### Stage 4: Leaderboard Panel
*DEP-ID:* `DEP-ENG-101`

**Steps:**
1. On `leaderboard_updated` event: render leaderboard as a vertical panel.
2. Animation: slide in from the right side over 500ms (Framer Motion `animate={{ x: 0 }}` from `initial={{ x: 300 }}`).
3. Display top 5 participants: rank, name, total score, score change ("+100").
4. Panel background: semi-transparent with DPA brand primary color accent.
5. Auto-dismiss: slide out after 5 seconds.

### Stage 5: Winner Reveal Animation
*DEP-ID:* `DEP-ENG-102`

**Steps:**
1. On `winner_reveal` event: full-screen overlay sequence.
2. Reveal order: 3rd place (zoom in from small, hold 2s) → 2nd place (zoom in, hold 2s) → 1st place (zoom in, hold 3s + confetti).
3. Each reveal: player name in large DPA-branded font, score underneath, glow animation.
4. Confetti: `canvas-confetti` library — fire from center, gold + DPA accent colors — 3 second burst.
5. Background: radial gradient from DPA primary color to black.
6. Auto-dismiss: fade out after 8 seconds total.

---

## 5. Primary Output Schema

**WebSocket Event Types:**

```json
{
  "type": "question_sent",
  "data": {
    "question_id": "uuid-q-001",
    "text": "What year was cognitive behavioral therapy formally developed?",
    "options": [
      {"key": "A", "text": "1952", "color": "#E74C3C"},
      {"key": "B", "text": "1960", "color": "#3498DB"},
      {"key": "C", "text": "1975", "color": "#2ECC71"},
      {"key": "D", "text": "1980", "color": "#F39C12"}
    ],
    "time_limit_seconds": 15
  }
}

{
  "type": "answer_distribution",
  "data": {
    "question_id": "uuid-q-001",
    "correct_answer": "B",
    "distribution": {
      "A": {"count": 12, "percentage": 24},
      "B": {"count": 28, "percentage": 56},
      "C": {"count": 5, "percentage": 10},
      "D": {"count": 5, "percentage": 10}
    }
  }
}

{
  "type": "leaderboard_updated",
  "data": {
    "top_5": [
      {"rank": 1, "name": "Sarah", "score": 2450, "change": "+150"},
      {"rank": 2, "name": "Mike", "score": 2100, "change": "+80"},
      {"rank": 3, "name": "Lisa", "score": 1900, "change": "+120"},
      {"rank": 4, "name": "James", "score": 1750, "change": "+100"},
      {"rank": 5, "name": "Emma", "score": 1600, "change": "+90"}
    ]
  }
}

{
  "type": "winner_reveal",
  "data": {
    "winners": [
      {"rank": 3, "name": "Lisa", "score": 1900},
      {"rank": 2, "name": "Mike", "score": 2100},
      {"rank": 1, "name": "Sarah", "score": 2450}
    ]
  }
}
```

---

## 6. Tasks

- [ ] **Task 1:** Build WebSocket client and state machine (`idle → question → distribution → leaderboard → winner → idle`).
- [ ] **Task 2:** Build `<QuestionDisplay />` component (question text, countdown bar, answer labels).
- [ ] **Task 3:** Build `<AnswerDistribution />` component (color-coded bars with animation).
- [ ] **Task 4:** Build `<LeaderboardPanel />` component (slide-in/out, top 5 display).
- [ ] **Task 5:** Build `<WinnerReveal />` component (3rd→2nd→1st reveal sequence with confetti).
- [ ] **Task 6:** Integrate overlay rendering into Studio Block's canvas compositing pipeline.
- [ ] **Task 7:** Apply DPA branding (FR-CA11-15) to all overlay components.
- [ ] **Task 8:** Add Trivianar WebSocket event emitter endpoint to `trivianar_engine.py`.

---

## 7. Acceptance Criteria

- [ ] **AC1 (Question Display):** Trivianar sends `question_sent`. Assert overlay renders question text + 4 labeled options + countdown bar in the lower third.
- [ ] **AC2 (Countdown):** Set 15-second timer. Assert countdown bar animates from full to empty in 15 seconds (±500ms).
- [ ] **AC3 (Answer Distribution):** After question closes with 56% on option B. Assert B's bar is wider than others. Assert correct answer (B) has glow effect.
- [ ] **AC4 (Leaderboard Slide-In):** Leaderboard event fires. Assert panel slides in from right within 500ms. Assert top 5 names, scores, and deltas visible. Assert auto-dismiss at 5 seconds.
- [ ] **AC5 (Winner Reveal):** Winner event fires. Assert 3rd place appears first (2s hold), then 2nd (2s hold), then 1st (3s hold + confetti). Assert confetti particles visible.
- [ ] **AC6 (DPA Branding):** Set coach brand color to `#2E86AB`. Assert overlay backgrounds, borders, and accent colors use `#2E86AB`.
- [ ] **AC7 (Recording Capture):** Record a stream with overlay active. Stop. Assert output video contains the overlay graphics composited with the webcam feed.
- [ ] **AC8 (Idle State):** No Trivianar events. Assert overlay renders nothing (transparent, no visual artifacts).

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-16 (Studio Block) | Internal | Overlay composites onto Studio Block's canvas. |
| FR-CA11-19 (Trivianar Engine) | Internal | Provides WebSocket events for overlay rendering. |
| FR-CA11-15 (DPA Branding) | Internal | Brand colors/fonts for overlay styling. |
| `canvas-confetti` | npm package | For winner reveal confetti animation. |
| `framer-motion` | npm package | For slide-in, fade, scale animations. |

---

## 9. Testing Strategy

### Unit Tests
- **State Machine:** Test all state transitions (idle→question→distribution→leaderboard→winner→idle). Assert invalid transitions are rejected.
- **Countdown Timer:** Mock 15-second timer. Assert progress value reaches 0 within ±100ms of target.
- **Distribution Bar Width:** Given `{A: 25%, B: 50%, C: 15%, D: 10%}`, assert bar widths are proportional.

### Integration Tests
- **Full Overlay Cycle:** Fire mock WebSocket events in sequence. Assert each overlay component renders and dismisses correctly.
- **Canvas Capture:** Render overlay on canvas → capture screenshot → assert overlay pixels are present at expected positions.

### Visual Review
- **Animation Quality:** Run full trivia cycle. Review: animation smoothness (60fps target), confetti visual quality, font legibility, color accuracy.
