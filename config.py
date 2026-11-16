import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "AsamAI - Autonomous B2B Agent Network"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database: Default to SQLite for easy local execution; PostgreSQL supported
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./asam_ai.db")
    
    # Vector Search & Reranking Settings
    EMBEDDING_DIMENSION: int = 1536  # Default dimension (or matched dynamically)
    VECTOR_TOP_K: int = 50
    RERANK_THRESHOLD: float = 0.75  # Stage 3 strict qualifying threshold
    MAX_NOTIFIED_AGENTS: int = 5    # Max fan-out per post
    
    # Feedback loop parameters
    FEEDBACK_LEARNING_RATE: float = 0.05
    FEEDBACK_NEGATIVE_THRESHOLD: int = 3  # Unengaged notifications before shift
    
    # Webhook & Security settings
    WEBHOOK_TIMEOUT_SECONDS: float = 5.0
    WEBHOOK_MAX_RETRIES: int = 3
    WEBHOOK_CIRCUIT_BREAKER_FAILURES: int = 3
    
    # Optional OpenAI Key for production embedding fallback
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)

settings = Settings()
