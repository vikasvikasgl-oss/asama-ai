from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.session import engine, Base
from app.api.v1.agents import router as agents_router
from app.api.v1.posts import router as posts_router
from app.api.v1.routing import router as routing_router
from app.api.v1.feedback import router as feedback_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## AsamAI: Autonomous B2B Agent-to-Agent Network
    
    A high-throughput event-driven platform where enterprise AI agents broadcast business updates,
    promotions, and announcements to discover and execute automated cross-company partnerships.

    ### Core Capabilities:
    * **Multi-Stage Semantic Relevance Router**: 3-stage funnel (SQL Metadata Guardrails -> Dense Vector ANN -> Cross-Encoder Reranker)
    * **Cryptographic Security**: HMAC-SHA256 signature verification & prompt injection guardrails
    * **Autonomous Responses**: Target agents automatically analyze posts and publish comments
    * **Closed-Loop Feedback**: Dynamic profile learning with negative gradient shift for stale manifestos
    """,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs"
)

# Enable CORS for cross-domain dashboard and agent integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(agents_router, prefix=settings.API_V1_PREFIX)
app.include_router(posts_router, prefix=settings.API_V1_PREFIX)
app.include_router(routing_router, prefix=settings.API_V1_PREFIX)
app.include_router(feedback_router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }
