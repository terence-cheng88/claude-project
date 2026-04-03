"""
API Router - REST endpoints for news aggregation
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator import SwarmCoordinator
from utils.news_sources import RSS_SOURCES, DEFAULTS


router = APIRouter()


class NewsRequest(BaseModel):
    """Request model for news aggregation"""
    topic: str
    max_articles: int = Query(default=10, ge=1, le=50)
    sources: str = Query(default="rss")


@router.post("/news", response_model=dict)
async def aggregate_news(request: NewsRequest):
    """
    Aggregate news for given topic using multi-agent swarm.
    """
    try:
        # Create coordinator
        coordinator = SwarmCoordinator(request_id=str(hash(request.topic)) % 10000)

        # Set defaults
        request.max_articles = min(request.max_articles, DEFAULTS["max_articles"])

        # Run swarm
        result = await coordinator.run(request.topic)

        return {
            "success": True,
            "request_id": coordinator.request_id,
            "topic": request.topic,
            "articles": result.get("articles", []),
            "total": len(result.get("articles", [])),
            "sources": result.get("sources_used", [])
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/news/{topic}", response_model=list)
async def get_topic_news(topic: str, limit: int = Query(default=10, ge=1)):
    """
    Get news for a specific topic.
    """
    try:
        coordinator = SwarmCoordinator()
        coordinator.topic = topic
        request = NewsRequest(topic=topic, max_articles=limit)
        result = await coordinator.run(topic)

        return result.get("articles", [])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get current swarm status"""
    return {
        "status": "ready",
        "agents_count": 6,
        "sources_count": len(RSS_SOURCES)
    }


@router.get("/sources")
async def list_sources():
    """List available news sources"""
    return {
        "sources": RSS_SOURCES
    }
