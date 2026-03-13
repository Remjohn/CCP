from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from .config import get_settings
from .ingress import router as ingress_router
from .api.assessment import router as assessment_router
from .api.analytics import router as analytics_router
from .core.graph import init_checkpointer, close_checkpointer
from .core.intelligence import intelligence_library
from .core.scheduler import scheduler
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # 1. Load Intelligence Library (Fail fast if invalid)
    intelligence_library.load()
    
    # 2. Init Graph Checkpointer
    await init_checkpointer()
    
    # 3. Start Scheduler
    scheduler.start()
    
    yield
    # Shutdown
    await scheduler.stop()
    await close_checkpointer()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(ingress_router)
app.include_router(assessment_router, prefix="/api/v1/assessment", tags=["Assessment"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
