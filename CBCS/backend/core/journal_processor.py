from backend.core.graph_db import context_graph
from backend.core.identity_models import IdentityVector
from backend.agents.perception.identity_scorers import build_identity_vector
from backend.agents.perception.cultural_detector import detect_cultural_frame
from backend.agents.temporal.chronos import analyze_temporal
from backend.agents.threat.sentinel import analyze_threats
import logging
import uuid

logger = logging.getLogger(__name__)


class JournalProcessor:
    """
    End-to-end journal processing pipeline.

    Pipeline stages (each gated by data thresholds):
    1. Aria extraction → entities + TTT state (existing)
    2. Cultural frame detection → CulturalFrame enum
    3. Identity vector computation → 12-dimensional IdentityVector
    4. Neo4j storage → timestamped IdentitySnapshot + temporal relationships
    5. Chronos temporal analysis (≥7 entries) → trends + change points + trajectory
    6. Sentinel threat detection (≥3 entries) → threat assessment + escalation phase
    7. Combined result for downstream (ritual selection, coach dashboard)
    """

    async def process_journal(self, user_id: str, text: str) -> dict:
        """
        Analyzes the journal text through the full Identity Engine pipeline.

        Returns a dict containing:
        - entities: extracted context premise entities
        - identity_vector: 12-dimensional identity vector
        - temporal_analysis: trends + change points + trajectory (if ≥7 entries)
        - threat_result: threat assessment + escalation phase (if ≥3 entries)
        """
        logger.info(f"Processing journal for user {user_id}...")
        entry_id = str(uuid.uuid4())

        result = {
            "entry_id": entry_id,
            "entities": [],
            "identity_vector": None,
            "temporal_analysis": None,
            "threat_result": None,
            "ttt_state": None,
        }

        try:
            # ── Stage 1: Entity Extraction via Aria ──
            # We now import Aria's output model. For backward compatibility,
            # attempt the existing aria.run() call, but gracefully handle
            # if the agent is not yet wired up.
            entities_data = []
            try:
                from backend.agents.perception.aria import agent as aria_agent
                aria_result = await aria_agent.run(text)
                extraction = aria_result.output.actionable_data
                entities_data = [e.model_dump() for e in extraction.entities]
                result["ttt_state"] = extraction.user_ttt_state
                result["entities"] = entities_data
                logger.info(f"Aria extracted {len(entities_data)} entities.")
            except Exception as aria_err:
                logger.warning(f"Aria extraction unavailable, proceeding with text-only: {aria_err}")

            # ── Stage 2: Cultural Frame Detection ──
            cultural_frame, cultural_confidence = detect_cultural_frame(text)
            logger.info(f"Cultural frame: {cultural_frame.value} (confidence: {cultural_confidence.value})")

            # ── Stage 3: Identity Vector Computation ──
            identity_vector = build_identity_vector(
                text=text,
                entities=entities_data,
                cultural_frame=cultural_frame,
                entry_id=entry_id,
            )
            result["identity_vector"] = identity_vector
            logger.info(
                f"Identity vector computed: confidence={identity_vector.confidence}, "
                f"agency={identity_vector.narrative.agency}, "
                f"autonomy={identity_vector.sdt.autonomy}"
            )

            # ── Stage 4: Neo4j Storage ──
            # 4a. Store context premise entities (temporal relationships)
            if entities_data:
                await context_graph.create_context_premise(
                    user_id, entities_data, entry_id=entry_id
                )

            # 4b. Store identity vector as IdentitySnapshot
            vector_dict = identity_vector.to_neo4j_dict()
            await context_graph.create_identity_vector(
                user_id, vector_dict, entry_id
            )
            logger.info(f"Identity vector stored in Neo4j for user {user_id}")

            # ── Stage 5: Chronos Temporal Analysis (≥7 entries) ──
            entry_count = await context_graph.get_entry_count(user_id)

            if entry_count >= 7:
                trajectory_data = await context_graph.get_identity_trajectory(user_id)
                temporal_analysis = analyze_temporal(trajectory_data)
                result["temporal_analysis"] = temporal_analysis
                logger.info(
                    f"Chronos analysis: trajectory={temporal_analysis.trajectory.value}, "
                    f"change_points={len(temporal_analysis.change_points)}, "
                    f"entries={temporal_analysis.entry_count}"
                )
            else:
                logger.info(f"Chronos skipped: only {entry_count} entries (need 7)")

            # ── Stage 6: Sentinel Threat Detection (≥3 entries) ──
            if entry_count >= 3:
                # Build trends dict for Sentinel
                trends_dict = {}
                if result["temporal_analysis"]:
                    for trend in result["temporal_analysis"].trends:
                        trends_dict[trend.dimension] = {
                            "direction": trend.direction.value,
                            "slope": trend.slope,
                        }

                trajectory_type = (
                    result["temporal_analysis"].trajectory
                    if result["temporal_analysis"]
                    else None
                )

                threat_result = analyze_threats(
                    text=text,
                    current_vector=identity_vector,
                    trajectory_type=trajectory_type,
                    trends=trends_dict,
                    entry_count=entry_count,
                )
                result["threat_result"] = threat_result

                if threat_result.get("requires_coach_alert"):
                    threat = threat_result["threat_assessment"]
                    logger.warning(
                        f"⚠️ COACH ALERT for user {user_id}: "
                        f"threat={threat.threat_type.value}, "
                        f"severity={threat.severity.value}, "
                        f"phase={threat_result['escalation_phase'].value}"
                    )
            else:
                logger.info(f"Sentinel skipped: only {entry_count} entries (need 3)")

            logger.info(f"Journal processing complete for user {user_id}.")
            return result

        except Exception as e:
            logger.error(f"Journal processing failed: {e}", exc_info=True)
            return result


# Global instance
journal_processor = JournalProcessor()

