from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "CBCS"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_SECRET_TOKEN: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    POSTGRES_URL: str  # Required for LangGraph Checkpointing

    # Groq
    GROQ_API_KEY: str

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # Runpod (Voice)
    RUNPOD_API_KEY: Optional[str] = None
    RUNPOD_ENDPOINT_ID: Optional[str] = None

    # Research
    TAVILY_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()
