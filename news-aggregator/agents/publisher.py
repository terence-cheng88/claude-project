"""
Publisher Agent - Formats and pushes results to UI
"""

import sys
import os
from datetime import datetime
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PublisherAgent:
    """
    Formats aggregation results and prepares for UI delivery.
    Handles WebSocket streaming and caching.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.name = "Publisher"

    def publish(self, results: dict) -> dict:
        """
        Format results for UI delivery.
        """
        print(f"[{self.name}] Publishing results. ..")

        # Build news items
        news_items = []
        processed_articles = results.get("processed_articles", [])
        sentiment = results.get("sentiment", [])

        for article in processed_articles:
            news_item = {
                "id": article.get("id", ""),
                "title": article.get("title", ""),
                "summary": article.get("summary", "")[:300] + "..." if len(article.get("summary", "")) > 300 else article.get("summary", ""),
                "url": article.get("url", ""),
                "published_at": article.get("published_at", ""),
                "source": article.get("source", ""),
                "category": article.get("category", ""),
                "sentiment": article.get("sentiment"),
                "is_spam": article.get("is_spam", False),
                "entities": article.get("entities", [])
            }
            news_items.append(news_item)

        # Build result
        final_result = {
            "request_id": self.request_id,
            "topic": results.get("topic", ""),
            "timestamp": datetime.now().isoformat(),
            "total_articles": len(news_items),
            "sources_used": list(set(a.get("source", "Unknown") for a in processed_articles)),
            "sentiment_breakdown": self._build_sentiment_breakdown(news_items),
            "articles": news_items
        }

        return final_result

    def _build_sentiment_breakdown(self, articles: List[dict]) -> dict:
        """Build sentiment distribution"""
        positive = sum(1 for a in articles if a.get("sentiment", 0) > 0.2)
        negative = sum(1 for a in articles if a.get("sentiment", 0) < -0.2)
        neutral = len(articles) - positive - negative

        return {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "average": sum(a.get("sentiment", 0) for a in articles) / len(articles) if articles else 0
        }

    def format_for_websocket(self, result: dict) -> str:
        """Format result as JSON string for WebSocket"""
        return result.model_dump_json() if hasattr(result, "model_dump") else str(result)
