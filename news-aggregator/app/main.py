"""
News Aggregator Application - FastAPI with Ruflo multi-agent swarm
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    app.state.settings = settings
    print(f"[Startup] {settings.app_name} v{settings.app_version} starting...")
    yield
    # Shutdown
    print(f"[Shutdown] {settings.app_name} shutting down...")


app = FastAPI(
    title="Ruflo News Aggregator",
    description="Multi-agent news aggregation demonstration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to Ruflo News Aggregator",
        "status": "running",
        "agents": ["Feeder", "Processor", "Sentiment", "Summarizer", "Publisher"],
        "docs": "/docs",
        "websocket": "/api/websocket"
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy"}


# Import and mount API router
from app import router
app.include_router(router.router, prefix="/api", tags=["API"])

# Import WebSocket handler
from app import websocket
app.websocket("/api/websocket")(websocket.connect)

# Add static files for frontend
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="frontend"), name="static")
