"""
News item model - aggregated news response
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NewsItem(BaseModel):
    """Aggregated news item with full metadata"""
    article: "Article"
    related_articles: list = Field(default_factory=list)
    topic_summary: Optional[str] = None
    is_fresh: bool = Field(default=False)  # Less than 30 mins old

    class Config:
        json_schema_extra = {
            "description": "A processed news item with related content"
        }


class AggregationResult(BaseModel):
    """Full aggregation result with swarm status"""
    request_id: str
    topic: str
    timestamp: datetime
    total_articles: int
    sources_used: list
    sentiment_breakdown: dict
    related_topics: list
    articles: list[NewsItem]

    class Config:
        json_schema_extra = {
            "description": "Complete result from multi-agent news aggregation"
        }
