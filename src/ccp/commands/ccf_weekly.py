"""
CCP Weekly Content Pipeline Command (ccf-weekly)
Task 2.13 — Orchestrates the full 19-command content production pipeline.

Pipeline:
  1. Check ContentCadence quota
  2. Load coach soul + topic queue
  3. ccf-analyze → generate 36 ideas
  4. For each idea (parallelized):
     a. Script generation (contrastive anti-draft pipeline)
     b. Inline minister checks (Identity, Relevance, Timing)
     c. Rewrite if ministers flag issues
  5. Validation Team gate (Sophia → Marcus → Chen)
  6. TillDone loop for failed pieces (max 3 retries)
  7. Push approved pieces to Operator review queue
  8. Record cadence
  9. Receipt Chain summary
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.agents.governance_ministers import GovernanceMinisters
from src.ccp.agents.humor_agent import HumorAgent
from src.ccp.agents.script_generator import ScriptGenerator
from src.ccp.commands.ccf_analyze import CCFAnalyzer, ContentIdea
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.extensions.content_cadence import ContentCadence
from src.ccp.models.coach_soul import CoachSoul
from src.ccp.services.contrastive_draft import ContrastiveDraftPipeline
from src.ccp.services.operator_review import OperatorReviewQueue
from src.ccp.services.soc_capture import SOCCapture
from src.ccp.services.validation_team import ValidationTeam


HUMOR_FORMATS = {"MEME", "POLL"}  # Formats that go through the Humor Agent
MAX_REWRITE_ATTEMPTS = 3
PARALLEL_BATCH_SIZE = 6  # Generate 6 pieces concurrently


class CCFWeeklyPipeline:
    """Orchestrates the full weekly content production pipeline."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.cadence = ContentCadence(coach_acronym=self.coach_acronym)
        self.analyzer = CCFAnalyzer(coach_acronym=self.coach_acronym)
        self.script_gen = ScriptGenerator(coach_acronym=self.coach_acronym)
        self.contrastive = ContrastiveDraftPipeline(coach_acronym=self.coach_acronym)
        self.humor_agent = HumorAgent(coach_acronym=self.coach_acronym)
        self.ministers = GovernanceMinisters()
        self.validation_team = ValidationTeam(coach_acronym=self.coach_acronym)
        self.review_queue = OperatorReviewQueue(coach_acronym=self.coach_acronym)
        self.soc = SOCCapture(coach_acronym=self.coach_acronym)

    async def run(self, target_count: int = 36) -> dict:
        """Execute the full weekly content pipeline.

        Args:
            target_count: Number of content pieces to produce

        Returns:
            Pipeline summary dict
        """
        start_time = time.monotonic()
        print(f"\n{'='*60}")
        print(f"  CCF WEEKLY PIPELINE: {self.coach_acronym}")
        print(f"  Target: {target_count} pieces")
        print(f"{'='*60}\n")

        # Step 1: Check cadence
        print("📊 Step 1/7: Checking content cadence...")
        can_produce, msg = self.cadence.can_produce(target_count)
        if not can_produce:
            print(f"   ❌ {msg}")
            return {"status": "blocked", "reason": msg}
        print(f"   ✅ {msg}")

        # Step 2: Load soul + topic queue
        print("📋 Step 2/7: Loading coach soul and topic queue...")
        soul = self._load_soul()
        topics = [seed.topic_summary for seed in self.soc.get_queue("queued")]
        print(f"   Soul: {soul.coach_name} (v{soul.version})")
        print(f"   Topics queued: {len(topics)}")

        # Step 3: Generate ideas
        print(f"💡 Step 3/7: Generating {target_count} content ideas...")
        batch = await self.analyzer.analyze(soul, topics, target_count)
        print(f"   Generated: {batch.total_count} ideas across {len(batch.format_distribution)} formats")
        print(f"   Format distribution: {batch.format_distribution}")

        # Steps 4-6: Generate + validate + rewrite loop
        print(f"✍️  Step 4-6/7: Generating, validating, and rewriting...")
        results = await self._process_all_ideas(soul, batch.ideas)

        approved = [r for r in results if r["status"] == "approved"]
        failed = [r for r in results if r["status"] == "failed"]
        print(f"   Approved: {len(approved)}/{len(results)}")
        print(f"   Failed after {MAX_REWRITE_ATTEMPTS} retries: {len(failed)}")

        # Step 7: Push to review queue
        print(f"📬 Step 7/7: Pushing {len(approved)} pieces to operator review queue...")
        for r in approved:
            self.review_queue.add(
                asset_id=r["asset_id"],
                format_type=r.get("format_type", "SCRP"),
                format_label=r.get("format_label", "Script"),
                topic=r.get("topic", ""),
                script=r["script"],
                validation_scores=r.get("validation_scores", {}),
            )

        # Record cadence
        self.cadence.record_batch(len(approved))

        elapsed = time.monotonic() - start_time
        summary = {
            "status": "completed",
            "coach": self.coach_acronym,
            "target": target_count,
            "generated": len(results),
            "approved": len(approved),
            "failed": len(failed),
            "elapsed_seconds": round(elapsed, 1),
            "cadence": self.cadence.get_status(),
        }

        # Final receipt
        self.receipt_chain.log(
            agent_id="ccf_weekly",
            action="complete_weekly_pipeline",
            input_summary=f"Target: {target_count} pieces",
            output_summary=f"Approved: {len(approved)}, Failed: {len(failed)}, Time: {elapsed:.0f}s",
            decision="completed",
            metadata=summary,
        )

        print(f"\n{'='*60}")
        print(f"  ✅ PIPELINE COMPLETE")
        print(f"  Approved: {len(approved)} | Failed: {len(failed)} | Time: {elapsed:.0f}s")
        print(f"  Review queue: {len(self.review_queue.get_pending())} pending")
        print(f"{'='*60}\n")

        return summary

    async def _process_all_ideas(
        self, soul: CoachSoul, ideas: list[ContentIdea]
    ) -> list[dict]:
        """Process all ideas in parallel batches."""
        results = []
        idea_dicts = [i.model_dump() for i in ideas]

        for batch_start in range(0, len(idea_dicts), PARALLEL_BATCH_SIZE):
            batch = idea_dicts[batch_start: batch_start + PARALLEL_BATCH_SIZE]
            batch_results = await asyncio.gather(
                *[self._process_single_idea(soul, idea) for idea in batch]
            )
            results.extend(batch_results)
            print(f"   Batch {batch_start // PARALLEL_BATCH_SIZE + 1}: {len(batch)} processed")

        return results

    async def _process_single_idea(self, soul: CoachSoul, idea: dict) -> dict:
        """Process a single idea through generation → ministers → validation → rewrite loop."""
        asset_id = idea.get("asset_id", "")

        for attempt in range(MAX_REWRITE_ATTEMPTS):
            # Generate
            if idea.get("format_type") in HUMOR_FORMATS:
                draft = await self.humor_agent.generate(soul, idea)
            else:
                draft = await self.contrastive.generate(soul, idea)

            script = draft.get("script", "")

            # Inline minister checks
            verdicts = await self.ministers.run_all(soul, script, idea.get("topic", ""))
            minister_issues = []
            for v in verdicts:
                if not v.passed:
                    minister_issues.extend(v.corrections)

            # If ministers flag issues, add to rewrite constraints and retry
            if minister_issues and attempt < MAX_REWRITE_ATTEMPTS - 1:
                idea["avoidance_constraints"] = idea.get("avoidance_constraints", []) + minister_issues
                continue

            # Validation Team gate
            validation = await self.validation_team.validate(
                soul, script, idea.get("format_label", "Script"), asset_id
            )

            if validation.passed:
                return {
                    "asset_id": asset_id,
                    "format_type": idea.get("format_type", "SCRP"),
                    "format_label": idea.get("format_label", "Script"),
                    "topic": idea.get("topic", ""),
                    "script": script,
                    "status": "approved",
                    "attempts": attempt + 1,
                    "validation_scores": {
                        "sophia": validation.sophia.score,
                        "marcus": validation.marcus.score,
                        "chen": validation.chen.score,
                        "overall": validation.overall_score,
                    },
                }

            # If validation fails, add rewrite instructions and retry
            if attempt < MAX_REWRITE_ATTEMPTS - 1:
                idea["avoidance_constraints"] = (
                    idea.get("avoidance_constraints", [])
                    + validation.combined_rewrite_instructions
                )

        # Failed after max retries
        return {
            "asset_id": asset_id,
            "format_type": idea.get("format_type", "SCRP"),
            "topic": idea.get("topic", ""),
            "status": "failed",
            "attempts": MAX_REWRITE_ATTEMPTS,
        }

    def _load_soul(self) -> CoachSoul:
        """Load the coach soul from disk."""
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if not soul_path.exists():
            raise FileNotFoundError(
                f"Coach soul not found at {soul_path}. Run Genesis Pipeline first."
            )
        data = json.loads(soul_path.read_text(encoding="utf-8"))
        return CoachSoul.model_validate(data)


async def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="CCP Weekly Content Pipeline")
    parser.add_argument("--coach", required=True, help="3-letter coach acronym")
    parser.add_argument("--count", type=int, default=36, help="Target content count")
    args = parser.parse_args()

    pipeline = CCFWeeklyPipeline(coach_acronym=args.coach.upper())
    result = await pipeline.run(target_count=args.count)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
