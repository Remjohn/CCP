from neo4j import GraphDatabase, AsyncGraphDatabase
from backend.config import get_settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class ContextGraph:
    """
    Neo4j graph database interface for the CBCS Context Premise Engine.
    
    Architecture: All relationships are temporal (timestamped + entry_id).
    MERGE is used for nodes (User, ContextNode, IdentitySnapshot).
    CREATE is used for relationships — preserving the full longitudinal history.
    Every journal entry produces separate timestamped edges, enabling:
      - Rolling window computation (Chronos Layer 3)
      - Change point detection (PELT algorithm)
      - Trajectory classification (Redemption/Contamination/Plateau)
    """

    # Allowed relationship types for context premise entities
    ALLOWED_CONTEXT_RELS = frozenset([
        "FIGHTS_AGAINST",  # User → Enemy
        "CRAVES",          # User → Dream (Ideal Self)
        "FEARS",           # User → Fear (Feared Self)
        "HAS_IDENTITY",    # User → Identity (Actual Self)
    ])

    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
        )

    async def close(self):
        await self.driver.close()

    async def init_indexes(self):
        """
        Creates indexes for time-series query performance.
        Safe to call multiple times (CREATE INDEX IF NOT EXISTS).
        """
        index_queries = [
            # Index on IdentitySnapshot for fast trajectory retrieval
            "CREATE INDEX identity_snapshot_user IF NOT EXISTS FOR (s:IdentitySnapshot) ON (s.user_id)",
            # Index on User node id
            "CREATE INDEX user_id IF NOT EXISTS FOR (u:User) ON (u.id)",
            # Index on ContextNode for deduplication
            "CREATE INDEX context_node_name IF NOT EXISTS FOR (n:ContextNode) ON (n.name)",
        ]
        async with self.driver.session() as session:
            for query in index_queries:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.warning(f"Index creation skipped (may already exist): {e}")
        logger.info("Neo4j indexes initialized for Identity Engine")

    async def create_user_node(self, user_id: str, name: str):
        """
        Creates or updates a User node in the graph.
        Uses MERGE — users are unique entities, not temporal.
        """
        query = """
        MERGE (u:User {id: $user_id})
        SET u.name = $name, u.updated_at = datetime()
        RETURN u
        """
        async with self.driver.session() as session:
            result = await session.run(query, user_id=user_id, name=name)
            record = await result.single()
            return record["u"]

    async def create_context_premise(
        self, user_id: str, entities: list[dict], entry_id: str = None
    ):
        """
        Creates context nodes and links them to the User with temporal properties.
        
        CRITICAL CHANGE from pre-Identity-Engine:
        - Nodes use MERGE (ContextNode is a concept, not temporal)
        - Relationships use CREATE (each journal entry produces a new edge)
        - Every relationship carries: timestamp, confidence, entry_id, source_quote
        
        This preserves full longitudinal history — Day 1 and Day 30 extractions
        of the same Fear exist as separate timestamped edges, enabling trajectory
        computation by Chronos.
        
        Entities structure: [{
            'type': 'Enemy',
            'name': 'Procrastination',
            'relationship': 'FIGHTS_AGAINST',
            'confidence': 'HIGH',         # HIGH/MEDIUM/LOW
            'evidence_quote': '...',       # source text
            'weight': 0.85                 # extraction confidence score
        }]
        """
        async with self.driver.session() as session:
            for entity in entities:
                rel_type = entity.get("relationship", "")
                if rel_type not in self.ALLOWED_CONTEXT_RELS:
                    logger.warning(f"Skipping invalid relationship type: {rel_type}")
                    continue

                # MERGE node (concept-level dedup), CREATE relationship (temporal edge)
                cypher = f"""
                MATCH (u:User {{id: $user_id}})
                MERGE (n:ContextNode {{name: $name}})
                SET n.type = $type
                CREATE (u)-[r:{rel_type} {{
                    timestamp: datetime(),
                    confidence: $confidence,
                    entry_id: $entry_id,
                    source_quote: $source_quote,
                    weight: $weight
                }}]->(n)
                RETURN r
                """
                await session.run(
                    cypher,
                    user_id=user_id,
                    name=entity["name"],
                    type=entity.get("type", "Unknown"),
                    confidence=entity.get("confidence", "LOW"),
                    entry_id=entry_id or "",
                    source_quote=entity.get("evidence_quote", ""),
                    weight=entity.get("weight", 0.0),
                )

    async def create_identity_vector(self, user_id: str, vector: dict, entry_id: str):
        """
        Stores a 12-dimensional identity vector as an IdentitySnapshot node
        linked to the User with a timestamped IDENTITY_VECTOR relationship.
        
        Each journal entry produces exactly one IdentitySnapshot.
        The vector contains scores from all Layer 2 sub-agents:
          - Narrative Identity: agency, communion, redemption_arc, meaning_making
          - Self-Discrepancy: actual_ideal_gap, actual_ought_gap, feared_self_proximity
          - SDT Need Profile: autonomy, competence, relatedness
          - Threat state: threat_level, active_defense
          - Metadata: cultural_frame, word_count, confidence
        
        Args:
            user_id: Telegram user ID
            vector: Dict containing all 12+ dimensional scores
            entry_id: Unique identifier for the journal entry
        """
        cypher = """
        MATCH (u:User {id: $user_id})
        CREATE (s:IdentitySnapshot {
            entry_id: $entry_id,
            user_id: $user_id,
            timestamp: datetime(),
            agency: $agency,
            communion: $communion,
            redemption_arc: $redemption_arc,
            meaning_making: $meaning_making,
            actual_ideal_gap: $actual_ideal_gap,
            actual_ought_gap: $actual_ought_gap,
            feared_self_proximity: $feared_self_proximity,
            hope_fear_balance: $hope_fear_balance,
            autonomy: $autonomy,
            competence: $competence,
            relatedness: $relatedness,
            threat_level: $threat_level,
            active_defense: $active_defense,
            cultural_frame: $cultural_frame,
            word_count: $word_count,
            confidence: $confidence
        })
        CREATE (u)-[r:IDENTITY_VECTOR {
            timestamp: datetime(),
            entry_id: $entry_id,
            confidence: $confidence
        }]->(s)
        RETURN s
        """
        params = {
            "user_id": user_id,
            "entry_id": entry_id,
            # Narrative Identity (Layer 2A)
            "agency": vector.get("agency", 0.0),
            "communion": vector.get("communion", 0.0),
            "redemption_arc": vector.get("redemption_arc", 0.0),
            "meaning_making": vector.get("meaning_making", 0.0),
            # Self-Discrepancy (Layer 2B)
            "actual_ideal_gap": vector.get("actual_ideal_gap", 0.0),
            "actual_ought_gap": vector.get("actual_ought_gap", 0.0),
            "feared_self_proximity": vector.get("feared_self_proximity", 0.0),
            "hope_fear_balance": vector.get("hope_fear_balance", 0.0),
            # SDT Need Profile (Layer 2C)
            "autonomy": vector.get("autonomy", 50),
            "competence": vector.get("competence", 50),
            "relatedness": vector.get("relatedness", 50),
            # Threat state (Layer 4)
            "threat_level": vector.get("threat_level", 0.0),
            "active_defense": vector.get("active_defense", "NONE"),
            # Metadata
            "cultural_frame": vector.get("cultural_frame", "DIRECT_INDIVIDUALIST"),
            "word_count": vector.get("word_count", 0),
            "confidence": vector.get("confidence", 0.0),
        }
        async with self.driver.session() as session:
            result = await session.run(cypher, **params)
            record = await result.single()
            logger.info(f"Identity vector stored for user {user_id}, entry {entry_id}")
            return record["s"] if record else None

    async def get_identity_trajectory(self, user_id: str, limit: int = 60) -> list[dict]:
        """
        Retrieves all IdentitySnapshot nodes for a user, ordered by timestamp.
        
        This is the primary data source for Chronos (Layer 3):
          - Rolling window computation requires ordered vectors
          - PELT change point detection requires time series
          - Trajectory classification requires the full arc
        
        Args:
            user_id: Telegram user ID
            limit: Max snapshots to retrieve (default 60 = 2 months of daily entries)
            
        Returns:
            List of dicts, each containing all 12+ dimensional scores + timestamp
        """
        cypher = """
        MATCH (u:User {id: $user_id})-[r:IDENTITY_VECTOR]->(s:IdentitySnapshot)
        RETURN s
        ORDER BY s.timestamp ASC
        LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(cypher, user_id=user_id, limit=limit)
            records = await result.data()
            # Convert Neo4j node properties to plain dicts
            return [dict(record["s"]) for record in records]

    async def get_context_history(
        self, user_id: str, rel_type: str, limit: int = 30
    ) -> list[dict]:
        """
        Retrieves temporal history of a specific relationship type for a user.
        Ordered by timestamp descending (most recent first).
        
        Useful for tracking how Enemies, Dreams, Fears evolve over time.
        """
        if rel_type not in self.ALLOWED_CONTEXT_RELS:
            logger.warning(f"Invalid relationship type for history query: {rel_type}")
            return []

        cypher = f"""
        MATCH (u:User {{id: $user_id}})-[r:{rel_type}]->(n:ContextNode)
        RETURN n.name AS name, n.type AS type,
               r.timestamp AS timestamp, r.confidence AS confidence,
               r.entry_id AS entry_id, r.source_quote AS source_quote,
               r.weight AS weight
        ORDER BY r.timestamp DESC
        LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(cypher, user_id=user_id, limit=limit)
            return await result.data()

    async def get_entry_count(self, user_id: str) -> int:
        """
        Returns the number of identity vector entries for a user.
        Used by journal_processor to determine which Chronos/Sentinel
        functions are eligible to run (minimum data thresholds).
        """
        cypher = """
        MATCH (u:User {id: $user_id})-[:IDENTITY_VECTOR]->(s:IdentitySnapshot)
        RETURN count(s) AS count
        """
        async with self.driver.session() as session:
            result = await session.run(cypher, user_id=user_id)
            record = await result.single()
            return record["count"] if record else 0

    # ─── Context Premise Engine Methods ──────────────────────────────

    async def create_audience_trigger_profile(
        self, user_id: str, profile_dict: dict, text_id: str
    ):
        """
        Stores an individual audience trigger profile as an AudienceSnapshot
        node linked to the User with a timestamped AUDIENCE_TRIGGER relationship.

        Each analyzed audience text produces one AudienceSnapshot.
        """
        cypher = """
        MATCH (u:User {id: $user_id})
        CREATE (a:AudienceSnapshot {
            text_id: $text_id,
            user_id: $user_id,
            timestamp: datetime(),
            rf_eagerness: $rf_eagerness,
            rf_vigilance: $rf_vigilance,
            rf_orientation: $rf_orientation,
            mft_care_harm: $mft_care_harm,
            mft_fairness_cheating: $mft_fairness_cheating,
            mft_loyalty_betrayal: $mft_loyalty_betrayal,
            mft_authority_subversion: $mft_authority_subversion,
            mft_sanctity_degradation: $mft_sanctity_degradation,
            mft_liberty_oppression: $mft_liberty_oppression,
            coping_phase: $coping_phase,
            herm_composite: $herm_composite,
            recon_prediction_error: $recon_prediction_error,
            auth_l_depth: $auth_l_depth,
            auth_proxy: $auth_proxy,
            confidence: $confidence,
            data_phase: $data_phase
        })
        CREATE (u)-[r:AUDIENCE_TRIGGER {
            timestamp: datetime(),
            text_id: $text_id
        }]->(a)
        RETURN a
        """
        params = {
            "user_id": user_id,
            "text_id": text_id,
            "rf_eagerness": profile_dict.get("rf_eagerness", 0.0),
            "rf_vigilance": profile_dict.get("rf_vigilance", 0.0),
            "rf_orientation": profile_dict.get("rf_orientation", "DUAL_DOMINANT"),
            "mft_care_harm": profile_dict.get("mft_care_harm", 0.0),
            "mft_fairness_cheating": profile_dict.get("mft_fairness_cheating", 0.0),
            "mft_loyalty_betrayal": profile_dict.get("mft_loyalty_betrayal", 0.0),
            "mft_authority_subversion": profile_dict.get("mft_authority_subversion", 0.0),
            "mft_sanctity_degradation": profile_dict.get("mft_sanctity_degradation", 0.0),
            "mft_liberty_oppression": profile_dict.get("mft_liberty_oppression", 0.0),
            "coping_phase": profile_dict.get("coping_phase", "PRE_CONTEMPLATION"),
            "herm_composite": profile_dict.get("herm_composite", 0.0),
            "recon_prediction_error": profile_dict.get("recon_prediction_error", 0.0),
            "auth_l_depth": profile_dict.get("auth_l_depth", "L1_PERFORMATIVE"),
            "auth_proxy": profile_dict.get("auth_proxy", 0.0),
            "confidence": profile_dict.get("confidence", "LOW"),
            "data_phase": profile_dict.get("data_phase", "COLD"),
        }
        async with self.driver.session() as session:
            result = await session.run(cypher, **params)
            record = await result.single()
            logger.info(f"Audience trigger profile stored for user {user_id}, text {text_id}")
            return record["a"] if record else None

    async def create_cohort_premise(self, segment_id: str, premise_dict: dict):
        """
        Stores an aggregated cohort-level context premise.
        Uses MERGE on segment_id — cohort premises are updated, not appended.
        """
        cypher = """
        MERGE (c:AudienceSegment {segment_id: $segment_id})
        SET c += $properties, c.updated_at = datetime()
        RETURN c
        """
        async with self.driver.session() as session:
            result = await session.run(
                cypher,
                segment_id=segment_id,
                properties=premise_dict,
            )
            record = await result.single()
            logger.info(f"Cohort premise stored for segment {segment_id}")
            return record["c"] if record else None

    async def get_audience_trajectory(
        self, user_id: str, limit: int = 100
    ) -> list[dict]:
        """
        Retrieves all AudienceSnapshot nodes for a user, ordered by timestamp.
        Used for temporal analysis of audience trigger profile evolution.
        """
        cypher = """
        MATCH (u:User {id: $user_id})-[r:AUDIENCE_TRIGGER]->(a:AudienceSnapshot)
        RETURN a
        ORDER BY a.timestamp ASC
        LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(cypher, user_id=user_id, limit=limit)
            records = await result.data()
            return [dict(record["a"]) for record in records]


# Global instance
context_graph = ContextGraph()
