# Voice Schema Index

This folder contains the production contracts for the premium voice system:

1. `dep_voice_001_voice_render_profile.schema.json`
   The stable coach-level rendering profile. Stores Voice DNA core, style state, growth delta, model strategy, and guardrails.

2. `dep_voice_002_expressive_memory_bank.schema.json`
   The coach-specific expressive archive used for retrieval, adapter training, and evaluation.

3. `dep_voice_003_prosody_score_packet.schema.json`
   The render-time score packet that turns message context into segment-by-segment voice directions.

4. `dep_voice_004_render_evaluation_packet.schema.json`
   The post-render validation contract used to decide if the output passes, needs retry, or should be escalated.

Recommended lifecycle:

`memory bank -> render profile -> prosody score packet -> render -> evaluation packet`
