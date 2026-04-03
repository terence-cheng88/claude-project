"""
News Aggregator Application - FastAPI with Ruflo multi-agent swarm
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ruflo News Aggregator",
    description="Multi-agent news aggregation demonstration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to Ruflo News Aggregator",
        "status": "running",
        "agents": ["Feeder", "Processor", "Sentiment", "Summarizer", "Publisher"],
        "docs": "/docs",
        "websocket": "/api/websocket"
    }


@app.get("/health")
async def health_check():
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
