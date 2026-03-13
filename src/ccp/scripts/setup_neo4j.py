"""
CCP Neo4j Context Premise Schema Setup
Task 3.03 — Creates the graph schema for client psychological profiles.

Node Types:
  - User (client)
  - Fear, Enemy, Dream, Ally, Victory, Pattern

Relationship Types:
  - TRIGGERS, OVERCOMES, CONNECTED_TO, BLOCKS, ENABLES

Each relationship carries an emotional_weight property (0.0-1.0).
"""

import os
from typing import Optional


SCHEMA_CYPHER = """
// Constraints for uniqueness
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.person_id IS UNIQUE;
CREATE CONSTRAINT fear_id IF NOT EXISTS FOR (f:Fear) REQUIRE f.id IS UNIQUE;
CREATE CONSTRAINT enemy_id IF NOT EXISTS FOR (e:Enemy) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT dream_id IF NOT EXISTS FOR (d:Dream) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT ally_id IF NOT EXISTS FOR (a:Ally) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT victory_id IF NOT EXISTS FOR (v:Victory) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT pattern_id IF NOT EXISTS FOR (p:Pattern) REQUIRE p.id IS UNIQUE;

// Indexes for fast traversal
CREATE INDEX user_coach IF NOT EXISTS FOR (u:User) ON (u.coach_acronym);
CREATE INDEX fear_user IF NOT EXISTS FOR ()-[r:HAS_FEAR]-() ON (r.user_id);
CREATE INDEX pattern_type IF NOT EXISTS FOR (p:Pattern) ON (p.pattern_type);
"""

# Cypher templates for common operations
CYPHER_TEMPLATES = {
    "create_user": """
        MERGE (u:User {person_id: $person_id})
        SET u.name = $name,
            u.coach_acronym = $coach_acronym,
            u.telegram_id = $telegram_id,
            u.created_at = datetime(),
            u.last_active = datetime()
        RETURN u
    """,
    "add_fear": """
        MATCH (u:User {person_id: $person_id})
        MERGE (f:Fear {id: $fear_id})
        SET f.description = $description,
            f.intensity = $intensity,
            f.source = $source,
            f.first_seen = coalesce(f.first_seen, datetime()),
            f.last_seen = datetime()
        MERGE (u)-[r:HAS_FEAR]->(f)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN f
    """,
    "add_enemy": """
        MATCH (u:User {person_id: $person_id})
        MERGE (e:Enemy {id: $enemy_id})
        SET e.description = $description,
            e.type = $enemy_type,
            e.first_seen = coalesce(e.first_seen, datetime()),
            e.last_seen = datetime()
        MERGE (u)-[r:FACES]->(e)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN e
    """,
    "add_dream": """
        MATCH (u:User {person_id: $person_id})
        MERGE (d:Dream {id: $dream_id})
        SET d.description = $description,
            d.clarity = $clarity,
            d.first_seen = coalesce(d.first_seen, datetime()),
            d.last_seen = datetime()
        MERGE (u)-[r:ASPIRES_TO]->(d)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN d
    """,
    "add_ally": """
        MATCH (u:User {person_id: $person_id})
        MERGE (a:Ally {id: $ally_id})
        SET a.description = $description,
            a.role = $role,
            a.first_seen = coalesce(a.first_seen, datetime()),
            a.last_seen = datetime()
        MERGE (u)-[r:SUPPORTED_BY]->(a)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN a
    """,
    "add_victory": """
        MATCH (u:User {person_id: $person_id})
        MERGE (v:Victory {id: $victory_id})
        SET v.description = $description,
            v.significance = $significance,
            v.date_achieved = $date_achieved,
            v.first_seen = coalesce(v.first_seen, datetime())
        MERGE (u)-[r:ACHIEVED]->(v)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN v
    """,
    "add_pattern": """
        MATCH (u:User {person_id: $person_id})
        MERGE (p:Pattern {id: $pattern_id})
        SET p.description = $description,
            p.pattern_type = $pattern_type,
            p.frequency = $frequency,
            p.first_seen = coalesce(p.first_seen, datetime()),
            p.last_seen = datetime()
        MERGE (u)-[r:EXHIBITS]->(p)
        SET r.emotional_weight = $emotional_weight,
            r.user_id = $person_id
        RETURN p
    """,
    "link_fear_enemy": """
        MATCH (f:Fear {id: $fear_id}), (e:Enemy {id: $enemy_id})
        MERGE (e)-[r:TRIGGERS]->(f)
        SET r.emotional_weight = $emotional_weight
        RETURN r
    """,
    "link_victory_fear": """
        MATCH (v:Victory {id: $victory_id}), (f:Fear {id: $fear_id})
        MERGE (v)-[r:OVERCOMES]->(f)
        SET r.emotional_weight = $emotional_weight
        RETURN r
    """,
    "get_full_premise": """
        MATCH (u:User {person_id: $person_id})
        OPTIONAL MATCH (u)-[rf:HAS_FEAR]->(f:Fear)
        OPTIONAL MATCH (u)-[re:FACES]->(e:Enemy)
        OPTIONAL MATCH (u)-[rd:ASPIRES_TO]->(d:Dream)
        OPTIONAL MATCH (u)-[ra:SUPPORTED_BY]->(a:Ally)
        OPTIONAL MATCH (u)-[rv:ACHIEVED]->(v:Victory)
        OPTIONAL MATCH (u)-[rp:EXHIBITS]->(p:Pattern)
        RETURN u,
            collect(DISTINCT {fear: f, weight: rf.emotional_weight}) AS fears,
            collect(DISTINCT {enemy: e, weight: re.emotional_weight}) AS enemies,
            collect(DISTINCT {dream: d, weight: rd.emotional_weight}) AS dreams,
            collect(DISTINCT {ally: a, weight: ra.emotional_weight}) AS allies,
            collect(DISTINCT {victory: v, weight: rv.emotional_weight}) AS victories,
            collect(DISTINCT {pattern: p, weight: rp.emotional_weight}) AS patterns
    """,
}


class ContextPremiseGraph:
    """Manages the Neo4j Context Premise graph for client profiles."""

    def __init__(self, coach_acronym: str, driver=None):
        self.coach_acronym = coach_acronym.upper()
        self._driver = driver

    def _get_driver(self):
        """Lazy-load Neo4j driver."""
        if self._driver is None:
            from neo4j import GraphDatabase
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "changeme")
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        return self._driver

    def setup_schema(self) -> None:
        """Create constraints and indexes."""
        driver = self._get_driver()
        with driver.session() as session:
            for statement in SCHEMA_CYPHER.strip().split(";"):
                stmt = statement.strip()
                if stmt:
                    session.run(stmt)
        print(f"✅ Neo4j schema initialized for {self.coach_acronym}")

    def create_user(self, person_id: str, name: str, telegram_id: str) -> dict:
        """Create or update a user node."""
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                CYPHER_TEMPLATES["create_user"],
                person_id=person_id,
                name=name,
                coach_acronym=self.coach_acronym,
                telegram_id=telegram_id,
            )
            return result.single().data()

    def add_dimension(
        self,
        person_id: str,
        dimension_type: str,
        dimension_id: str,
        description: str,
        emotional_weight: float = 0.5,
        **kwargs,
    ) -> dict:
        """Add a Context Premise dimension (Fear, Enemy, Dream, Ally, Victory, Pattern)."""
        template_key = f"add_{dimension_type.lower()}"
        if template_key not in CYPHER_TEMPLATES:
            raise ValueError(f"Unknown dimension type: {dimension_type}")

        driver = self._get_driver()
        params = {
            "person_id": person_id,
            f"{dimension_type.lower()}_id": dimension_id,
            "description": description,
            "emotional_weight": emotional_weight,
            **kwargs,
        }

        with driver.session() as session:
            result = session.run(CYPHER_TEMPLATES[template_key], **params)
            return result.single().data() if result.peek() else {}

    def get_full_premise(self, person_id: str) -> dict:
        """Get the complete Context Premise for a client."""
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                CYPHER_TEMPLATES["get_full_premise"],
                person_id=person_id,
            )
            record = result.single()
            if not record:
                return {}
            return record.data()

    def get_narrative(self, person_id: str) -> str:
        """Get the Context Premise as a clean narrative (for Notion display)."""
        premise = self.get_full_premise(person_id)
        if not premise:
            return "No context available yet."

        parts = []
        fears = [f for f in premise.get("fears", []) if f.get("fear")]
        if fears:
            fear_descriptions = [f["fear"].get("description", "") for f in fears]
            parts.append(f"**Currently navigating:** {', '.join(fear_descriptions)}")

        victories = [v for v in premise.get("victories", []) if v.get("victory")]
        if victories:
            victory_descriptions = [v["victory"].get("description", "") for v in victories]
            parts.append(f"**Recent wins:** {', '.join(victory_descriptions)}")

        dreams = [d for d in premise.get("dreams", []) if d.get("dream")]
        if dreams:
            dream_descriptions = [d["dream"].get("description", "") for d in dreams]
            parts.append(f"**Moving toward:** {', '.join(dream_descriptions)}")

        patterns = [p for p in premise.get("patterns", []) if p.get("pattern")]
        if patterns:
            pattern_descriptions = [p["pattern"].get("description", "") for p in patterns]
            parts.append(f"**Patterns noticed:** {', '.join(pattern_descriptions)}")

        return "\n".join(parts) if parts else "Building context from conversations..."

    def close(self) -> None:
        """Close the Neo4j driver."""
        if self._driver:
            self._driver.close()
