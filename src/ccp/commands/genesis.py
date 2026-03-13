"""
CCP Genesis Pipeline Command (ccf-init)
Task 1.14 — Orchestrates the full coach onboarding sequence.

Pipeline Steps:
  1. Scaffold coach directory
  2. Register coach in coach_registry.json
  3. Process Sacred Audio uploads → Groq transcription
  4. Extract TTT baseline (Voice DNA)
  5. Process onboarding interview → Kimya identity extraction
  6. Score Leadership Traits (12 dimensions)
  7. Assemble and validate coach_soul.json
  8. Log everything to Receipt Chain

Usage:
    python -m src.ccp.commands.genesis --coach-name "Nadia Lefèvre" --acronym NDL
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.agents.kimya_processor import KimyaProcessor
from src.ccp.agents.leadership_scorer import LeadershipTraitScorer
from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_registry import CoachRegistry
from src.ccp.models.coach_soul import CoachSoul
from src.ccp.scripts.scaffold_coach import scaffold_coach
from src.ccp.services.groq_transcriber import GroqTranscriber
from src.ccp.services.ttt_extractor import TTTExtractor


class GenesisPipeline:
    """Orchestrates the full coach onboarding process."""

    def __init__(self, coach_name: str, acronym: str, base_dir: str = "./coaches"):
        self.coach_name = coach_name
        self.acronym = acronym.upper()
        self.base_dir = Path(base_dir)
        self.coach_dir = self.base_dir / self.acronym

        # Initialize services
        self.receipt_chain = ReceiptChain(
            coach_acronym=self.acronym,
            log_dir=str(self.coach_dir / "logs" / "receipt_chain"),
        )
        self.asset_gen = AssetIDGenerator(coach_acronym=self.acronym)
        self.transcriber = GroqTranscriber()
        self.ttt_extractor = TTTExtractor()
        self.kimya = KimyaProcessor()
        self.leadership_scorer = LeadershipTraitScorer()

    async def run(
        self,
        audio_files: Optional[list[str]] = None,
        interview_transcript: Optional[str] = None,
        research_brief: Optional[str] = None,
    ) -> CoachSoul:
        """Execute the full Genesis Pipeline.

        Args:
            audio_files: Paths to Sacred Audio recordings (if already uploaded)
            interview_transcript: The onboarding interview text
            research_brief: Pre-meeting research about the coach

        Returns:
            Completed CoachSoul profile
        """
        print(f"\n{'='*60}")
        print(f"  GENESIS PIPELINE: {self.coach_name} ({self.acronym})")
        print(f"{'='*60}\n")

        # Step 1: Scaffold
        print("📁 Step 1/7: Scaffolding coach directory...")
        self._scaffold()

        # Step 2: Initialize registry and soul
        print("📋 Step 2/7: Initializing registry and soul profile...")
        registry = self._init_registry()
        soul = self._init_soul()

        # Step 3: Transcribe Sacred Audio
        transcripts = []
        if audio_files:
            print(f"🎙️  Step 3/7: Transcribing {len(audio_files)} Sacred Audio files...")
            transcripts = await self._transcribe_audio(audio_files)
        else:
            print("⏭️  Step 3/7: No audio files provided (use upload endpoint first)")

        # Step 4: Extract Voice DNA (TTT baseline)
        if transcripts:
            print("🧬 Step 4/7: Extracting Voice DNA (TTT baseline)...")
            voice_dna = self.ttt_extractor.extract(transcripts)
            soul.voice_dna = voice_dna
            self.receipt_chain.log(
                agent_id="ttt_extractor",
                action="extract_voice_dna",
                input_summary=f"Extracted from {len(transcripts)} transcripts ({sum(len(t) for t in transcripts)} chars)",
                output_summary=f"Rhythm: {voice_dna.sentence_rhythm}, Metaphors: {voice_dna.metaphor_patterns}",
                decision="completed",
                metadata={"transcript_count": len(transcripts)},
            )
            print(f"   Rhythm: {voice_dna.sentence_rhythm}")
            print(f"   Metaphors: {voice_dna.metaphor_patterns}")
            print(f"   Humor: {voice_dna.humor_style}")
        else:
            print("⏭️  Step 4/7: Skipping (no transcripts)")

        # Step 5: Kimya identity extraction
        if interview_transcript:
            print("🔮 Step 5/7: Running Kimya identity extraction...")
            extracted = await self.kimya.process_interview(
                transcript=interview_transcript,
                research_brief=research_brief,
            )
            soul = self.kimya.apply_to_soul(soul, extracted)
            self.receipt_chain.log(
                agent_id="kimya",
                action="extract_identity",
                input_summary=f"Interview transcript ({len(interview_transcript)} chars)",
                output_summary=f"Philosophy: {soul.coaching_philosophy[:80]}...",
                decision="completed",
                metadata={"fields_extracted": list(extracted.keys())},
            )
            print(f"   Philosophy: {soul.coaching_philosophy[:100]}...")
            print(f"   Tribe: {soul.tribe_archetype}")
            print(f"   Core message: {soul.core_message[:100]}...")
        else:
            print("⏭️  Step 5/7: Skipping (no interview transcript)")

        # Step 6: Leadership Trait Scoring
        if transcripts or interview_transcript:
            print("📊 Step 6/7: Scoring Leadership Traits (12 dimensions)...")
            scores, evidence = await self.leadership_scorer.score(
                sacred_audio_transcripts=transcripts or ["[No Sacred Audio provided]"],
                interview_transcript=interview_transcript or "[No interview provided]",
            )
            soul.leadership_scores = scores

            # Save leadership report
            report = self.leadership_scorer.format_report(scores, evidence)
            report_path = self.coach_dir / "config" / "leadership_report.md"
            report_path.write_text(report, encoding="utf-8")

            self.receipt_chain.log(
                agent_id="minister_identity",
                action="score_leadership_traits",
                input_summary=f"Scored from {len(transcripts)} transcripts + interview",
                output_summary=f"Dominant: {scores.dominant_trait()}, Balance: {scores.trait_balance_ratio():.0%}",
                decision="completed",
                metadata={
                    "scores": scores.model_dump(),
                    "dominant_trait": scores.dominant_trait(),
                    "weak_traits": scores.get_weak_traits(),
                    "strong_traits": scores.get_strong_traits(),
                },
            )
            print(f"   Dominant: {scores.dominant_trait().replace('_', ' ').title()}")
            print(f"   Balance: {scores.trait_balance_ratio():.0%}")
            print(f"   Weak: {scores.get_weak_traits()}")
            print(f"   Strong: {scores.get_strong_traits()}")
        else:
            print("⏭️  Step 6/7: Skipping (no input data)")

        # Step 7: Save and finalize
        print("💾 Step 7/7: Saving coach_soul.json...")
        self._save_soul(soul)

        # Final receipt
        genesis_complete = soul.is_genesis_complete()
        self.receipt_chain.log(
            agent_id="genesis_pipeline",
            action="complete_genesis",
            input_summary=f"Coach: {self.coach_name} ({self.acronym})",
            output_summary=f"Genesis {'COMPLETE' if genesis_complete else 'PARTIAL'} — v{soul.version}",
            decision="completed" if genesis_complete else "partial",
            metadata={
                "genesis_complete": genesis_complete,
                "soul_version": soul.version,
                "fields_populated": [
                    f for f in ["voice_dna", "philosophy", "leadership"]
                    if getattr(soul, {
                        "voice_dna": "voice_dna",
                        "philosophy": "coaching_philosophy",
                        "leadership": "leadership_scores"
                    }.get(f, ""), None)
                ],
            },
        )

        print(f"\n{'='*60}")
        if genesis_complete:
            print(f"  ✅ GENESIS COMPLETE: {self.coach_name} ({self.acronym}-0000)")
        else:
            print(f"  ⚠️  GENESIS PARTIAL: Some fields still empty")
            print(f"     Re-run with missing inputs to complete.")
        print(f"  📄 Soul: {self.coach_dir / 'config' / 'coach_soul.json'}")
        print(f"  📋 Registry: {self.coach_dir / 'config' / 'coach_registry.json'}")
        print(f"  📊 Receipt Chain: {self.receipt_chain.chain_length()} entries")
        print(f"{'='*60}\n")

        return soul

    def _scaffold(self) -> None:
        """Step 1: Create the coach directory structure."""
        try:
            scaffold_coach(self.coach_name, self.acronym, str(self.coach_dir))
            self.receipt_chain.log(
                agent_id="genesis_pipeline",
                action="scaffold_directory",
                output_summary=f"Created at {self.coach_dir}",
                decision="completed",
            )
        except FileExistsError:
            print(f"   Directory already exists, continuing...")
            self.receipt_chain.log(
                agent_id="genesis_pipeline",
                action="scaffold_directory",
                output_summary=f"Already exists at {self.coach_dir}",
                decision="skipped",
            )

    def _init_registry(self) -> CoachRegistry:
        """Step 2a: Load or create the coach registry."""
        registry_path = self.coach_dir / "config" / "coach_registry.json"
        if registry_path.exists():
            data = json.loads(registry_path.read_text(encoding="utf-8"))
            return CoachRegistry.model_validate(data)
        else:
            registry = CoachRegistry(
                coach_name=self.coach_name,
                coach_acronym=self.acronym,
                coach_id=f"{self.acronym}-0000",
                notion_token_ref=f"NOTION_TOKEN_{self.acronym}",
                supabase_bucket=f"coach-{self.acronym.lower()}",
            )
            registry_path.parent.mkdir(parents=True, exist_ok=True)
            registry_path.write_text(
                registry.model_dump_json(indent=2), encoding="utf-8"
            )
            return registry

    def _init_soul(self) -> CoachSoul:
        """Step 2b: Load or create the coach soul profile."""
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        if soul_path.exists():
            data = json.loads(soul_path.read_text(encoding="utf-8"))
            return CoachSoul.model_validate(data)
        else:
            return CoachSoul(
                coach_name=self.coach_name,
                coach_id=f"{self.acronym}-0000",
            )

    async def _transcribe_audio(self, audio_files: list[str]) -> list[str]:
        """Step 3: Transcribe Sacred Audio files."""
        transcripts = []
        for i, audio_path in enumerate(audio_files):
            print(f"   [{i+1}/{len(audio_files)}] Transcribing {Path(audio_path).name}...")
            try:
                result = self.transcriber.transcribe_file(audio_path)
                transcripts.append(result.text)

                asset_id = self.asset_gen.generate(AssetType.SACRED_AUDIO)
                self.receipt_chain.log(
                    agent_id="groq_transcriber",
                    action="transcribe_sacred_audio",
                    asset_id=asset_id,
                    input_summary=f"File: {Path(audio_path).name}",
                    output_summary=f"Transcribed: {len(result.text)} chars, {result.duration_seconds:.1f}s audio, {result.processing_time_ms:.0f}ms processing",
                    decision="completed",
                    metadata={
                        "duration_seconds": result.duration_seconds,
                        "processing_time_ms": result.processing_time_ms,
                        "language": result.language,
                    },
                )
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                self.receipt_chain.log(
                    agent_id="groq_transcriber",
                    action="transcribe_sacred_audio",
                    input_summary=f"File: {Path(audio_path).name}",
                    output_summary=f"FAILED: {str(e)}",
                    decision="failed",
                )

        return transcripts

    def _save_soul(self, soul: CoachSoul) -> None:
        """Step 7: Save the completed coach_soul.json."""
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        soul_path.parent.mkdir(parents=True, exist_ok=True)
        soul_path.write_text(soul.model_dump_json(indent=2), encoding="utf-8")


async def main():
    """CLI entry point for the Genesis Pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="CCP Genesis Pipeline (ccf-init)")
    parser.add_argument("--coach-name", required=True, help="Full coach name")
    parser.add_argument("--acronym", required=True, help="3-letter coach acronym")
    parser.add_argument("--audio", nargs="*", help="Paths to Sacred Audio files")
    parser.add_argument("--interview", help="Path to interview transcript file")
    parser.add_argument("--research", help="Path to research brief file")
    parser.add_argument("--base-dir", default="./coaches", help="Base directory for coach instances")

    args = parser.parse_args()

    # Validate acronym
    acronym = args.acronym.upper()
    if len(acronym) != 3 or not acronym.isalpha():
        parser.error("Acronym must be exactly 3 alphabetic characters")

    # Load text files if provided
    interview_text = None
    if args.interview:
        interview_text = Path(args.interview).read_text(encoding="utf-8")

    research_text = None
    if args.research:
        research_text = Path(args.research).read_text(encoding="utf-8")

    # Run the pipeline
    pipeline = GenesisPipeline(
        coach_name=args.coach_name,
        acronym=acronym,
        base_dir=args.base_dir,
    )

    soul = await pipeline.run(
        audio_files=args.audio,
        interview_transcript=interview_text,
        research_brief=research_text,
    )


if __name__ == "__main__":
    asyncio.run(main())
