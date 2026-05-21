---
type: architecture-crosswalk
author: Codex synthesis for CCP
date: 2026-05-05
status: Working Draft
dependencies:
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Meaning_Primitive_Registry_Spec.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Experience_Primitive_Registry_Spec.md
---

# Primitive Crosswalk Map

## 1. Purpose

This document exists because some primitive concepts influence both:

- what we produce
- and what the user experiences while producing or receiving it

That does not mean they should be stored in one registry.

It means we need a crosswalk.

The rule is:

**same territory can exist in both registries if the implementation role is different.**

Representative examples in this document should be listed in descending original audit `MCDA` order whenever possible so the table can be skimmed quickly.

## 2. Crosswalk Rules

### Rule 1

If the primitive mainly changes output meaning, it belongs in the meaning registry.

### Rule 2

If the primitive mainly changes user state, interface behavior, or adoption flow, it belongs in the experience registry.

### Rule 3

If the same idea matters in both places, keep two entries and link them explicitly.

## 3. Crosswalk Table

| Territory | Meaning Registry Role | Experience Registry Role | Representative Meaning Primitives | Representative Experience Primitives |
|---|---|---|---|---|
| Attention routing | Control what the audience notices inside content | Control what the user notices inside the product | `Composition is Eye-Path Engineering` `198`, `Hierarchy as Semantic Attention Routing` `192` | `Visual Emphasis Must Be Intentional` `196`, `Visceral Hooking` `175`, `Bring the Data Forward` `170` |
| Trust and permission | Build trust in the message | Build trust in the product and flow | `Matching Principle` `192`, `Connection Before Content` `190` | `Design for Lived Use, Not Abstract Intent` `194`, `Dignity Reduces Friction Better Than Force` `189`, `The Trust Architecture` `170` |
| Emotional pacing | Shape tension and release in outputs | Shape pressure and recovery in product moments | `Emotional Journey Mapping` `196`, `Silence as a Positive Narrative Device` `196`, `Contrast Architecture` `189` | `White Hat -> Black Hat -> White Hat Emotional Sequencing` `196`, `Possible-Win Scarcity` `186`, `Signature Moment` `170` |
| Authority and delivery | Improve the coach's actual take and voice | Improve how the system frames, scores, and reinforces authority | `Superobjective` `194`, `Magic As If / Particularization` `192`, `Directed Emotional Stance` `190` | `Write for the Distracted Ear` `197`, `Audience-of-One Intimacy` `196`, `Reflective Scoring` `175` |
| Social proof | Make content socially compelling and discussable | Turn usage into share, vote, side-taking, and silent referral | `Hyper-Specificity Anchoring` `195`, `Change Choreography` `194`, `DataPOV` `192` | `Social Treasures + Group Quests` `194`, `Social Capital and Self-Esteem Economy` `186`, `Identity-Driven Social Proof` `180` |
| Progression | Structure the content journey or learning arc | Structure the app journey and challenge continuation | `Throughline` `196`, `Journey Architecture and Threshold Design` `184`, `Recommendation Trees` `178` | `First Major Win-State Before Social Expansion` `197`, `Discover -> On-board -> Immerse -> Master -> Replay` `178`, `Long Loops for Habit Formation` `145` |
| Human vividness | Make output feel real, specific, and not AI-flat | Make the whole product feel alive, premium, and human | `Audience-of-One Intimacy` `196`, `The Mix` `191`, `Humanize Information` `187` | `Placebo Onboarding` `180`, `Visceral Hooking` `175`, `Haptic and Visual Micro-Feedback` `170` |
| Recovery and repair | Repair weak arguments or flat storytelling | Repair churn moments and protect ego after low scores | `Looping for Understanding` `192`, `Pre-Conversation Architecture` `188` | `Possible-Win Scarcity` `186`, `Richter Rescue` `165`, `Behavioral Forgiveness` `160` |

## 4. Shelf-Level Crosswalk Notes

## 4.1 Humor and Comedy

Meaning-first:

- `Hyper-Specificity Anchoring` - `195`
- `The Mix` - `191`
- `Directed Emotional Stance` - `190`

Experience carryover:

- stronger topic briefs
- better social clip energy
- better premium non-generic feel

## 4.2 Acting and Performance

Meaning-first:

- `Superobjective` - `194`
- `Magic As If / Particularization` - `192`
- `Pinch and Ouch` - `190`

Experience carryover:

- better guided pre-state
- better score feedback framing
- better coaching confidence before recording

## 4.3 Public Speaking and Storytelling

Meaning-first:

- `Perception and Behavioral Guidance as a Unified Stack` - `199`
- `Throughline` - `196`
- `Emotional Journey Mapping` - `196`
- `Connection Before Content` - `190`

Experience carryover:

- clearer entry flows
- better challenge arc
- stronger opening and closing moments

## 4.4 Psychology and Communication

Meaning-first:

- `Identification Builds the Bridge` - `196`
- `Matching Principle` - `192`
- `Looping for Understanding` - `192`
- `Deep Questions` - `190`

Experience carryover:

- better agent replies
- better supervisor pairing behavior
- better recovery messages

## 4.5 Design, Photography, and Sound

Meaning-first:

- `Composition is Eye-Path Engineering` - `198`
- `Workflow Creates Aesthetics` - `198`
- `Write for the Distracted Ear` - `197`
- `Visual Emphasis Must Be Intentional` - `196`

Experience carryover:

- better mini app visual hierarchy
- better score reveal choreography
- better sonic trust and pacing

## 4.6 Experience Engineering

Experience-first:

- `First Major Win-State Before Social Expansion` - `197`
- `White Hat -> Black Hat -> White Hat Emotional Sequencing` - `196`
- `Social Treasures + Group Quests` - `194`
- `Monitor Attachment + Alfred Personalization` - `193`

Meaning carryover:

- helps shape how content modes are sequenced
- helps shape how debates, tierlists, and reaction formats are introduced

## 5. What to Do Operationally

When a primitive appears in both worlds:

1. create a meaning entry if it changes generated output
2. create an experience entry if it changes product behavior
3. link them with a shared `crosswalk_id`

Examples:

- `Audience-of-One Intimacy`
  - meaning entry: voice-note writing and delivery style
  - experience entry: how briefings, reminders, and score feedback are voiced

- `Composition is Eye-Path Engineering`
  - meaning entry: visual content generation and CVE validators
  - experience entry: debate screens, score cards, share cards, and entry hierarchy

This keeps implementation clean while still preserving conceptual unity.

## 6. Final Position

The crosswalk exists to prevent two bad outcomes:

1. flattening everything into one registry
2. pretending the registries never touch each other

The correct architecture is:

- separate registries
- explicit shared concepts
- separate implementation value

That is the cleanest way to keep both depth and buildability.
