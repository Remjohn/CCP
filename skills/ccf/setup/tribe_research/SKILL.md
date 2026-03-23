---
name: Tribe Research Skills (4-Skill Architecture)
description: FR0B — 4 specialist tribe research skills producing H11 Tribe Dossier. Lexicon, Humor, Emotional, Social research with cross-dimensional convergence analysis.
---

# Tribe Research Skills — SKILL.md

## Architecture

FR0B uses a 4-skill architecture. Each skill operates independently on different research dimensions, then the Guardian Agent synthesizes results.

| Skill | Section | Focus | Academic Grounding |
|---|---|---|---|
| `tribe-lexicon-research` | A — Cultural Artifacts | Slang, heroes/enemies, inside jokes | Koppel et al. 2009 |
| `tribe-humor-research` | B — Humor DNA Profile | Comedy styles, meme formats, taboos | McGraw & Warren 2010 |
| `tribe-emotional-research` | C — Emotional Landscape | L3 fears, aspirations, triggers | LIWC-22, Perlis 2016 |
| `tribe-social-research` | D — Social Architecture | Rules, status signals, boundaries | Tajfel & Turner 1979 |

## DEP-ID Declarations

| DEP-ID | Direction | Description |
|---|---|---|
| `H11` | **PRODUCES** | Tribe Dossier (25-30 page verbatim corpus) |
| `DEP-ENG-050` | **CONSUMES** | Business Intelligence Summary (audience targets) |

## Quality Gates

| Gate | Threshold | Pass | Fail |
|---|---|---|---|
| Volume Verification | ≥25 pages | Pipeline continues | FAILED — identify under-volume skill |
| Verbatim Ratio | ≥70% direct quotes | AUTHENTICATED | FAILED or PROVISIONAL if near-miss |

## Core Principle

**Archive, don't analyze.** Every entry must be a direct verbatim quote with provenance. Paraphrased summaries fail the Verbatim Ratio Test.

## Receipt Chain Guard

| Stage | Receipt Fields |
|---|---|
| **INGEST** | `platform_targets[]`, `audience_segment`, `dep_eng_050_version` |
| **Per-skill EMIT** (×4) | `section`, `verbatim_ratio`, `volume_pages`, `source_count` |
| **Synthesis EMIT** | `total_pages`, `aggregate_verbatim_ratio`, `convergence_events_count`, `verdict` |
