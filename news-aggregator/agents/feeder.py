"""
News Feeder Agent - Fetches articles from RSS/API sources
"""

import asyncio
import feedparser
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.news_sources import RSS_SOURCES


class NewsFeederAgent:
    """
    Feeds news articles from multiple RSS/API sources.
    Each instance handles a specific source.
    """

    def __init__(self, request_id: str, index: int):
        self.request_id = request_id
        self.index = index
        self.name = f"Feeder-{index}"
        self.base_url = None

    async def fetch_articles(self, topic: str, max_articles: int = 10) -> dict:
        """
        Fetch articles from assigned source.
        """
        articles = []
        print(f"[{self.name}] Fetching articles for topic: {topic}...")

        # Select RSS source based on topic
        rss_url = self._select_rss_source(topic, max_articles)

        try:
            # Parse RSS feed
            feed = feedparser.parse(rss_url)

            for entry in feed.entries[:max_articles]:
                article = {
                    "id": entry.get("id", entry.get("link", "")),
                    "title": entry.get("title", ""),
                    "summary": entry.get("description", "")[:500],  # Truncate
                    "url": entry.get("link", rss_url),
                    "published_at": self._parse_date(entry.get("published", "")),
                    "source": feed.get("feed", {}).get("title", rss_url),
                    "category": self._categorize(entry.get("title", topic)),
                    "raw": entry
                }
                articles.append(article)

            return {
                "status": "success",
                "source": self.name,
                "article_count": len(articles),
                "articles": articles
            }

        except Exception as e:
            return {
                "status": "error",
                "source": self.name,
                "error": str(e),
                "articles": []
            }

    def _select_rss_source(self, topic: str, max_articles: int) -> str:
        """Select appropriate RSS source based on topic"""
        # Filter by topic relevance
        tech_keywords = ["ai", "tech", "techcrunch", "bloomberg", "verge", "wired"]
        finance_keywords = ["reuters", "finance", "market", "stocks"]

        # Select RSS by topic relevance
        for source in RSS_SOURCES:
            if any(kw in topic.lower() for kw in tech_keywords):
                return source["url"]
            elif any(kw in topic.lower() for kw in finance_keywords):
                return source["url"]
            elif source["category"] == "tech":
                return source["url"]

        # Default to first available RSS
        return RSS_SOURCES[0]["url"]

    def _parse_date(self, date_str: str) -> str:
        """Parse various date formats to ISO string"""
        if not date_str:
            return datetime.now().isoformat()
        try:
            # Try parsing common formats
            for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"]:
                try:
                    dt = datetime.strptime(date_str[:19], fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            return datetime.now().isoformat()
        except Exception:
            return datetime.now().isoformat()

    def _categorize(self, title: str, topic: str) -> str:
        """Categorize article based on title and topic"""
        title_lower = title.lower()
        topic_lower = topic.lower()

        if any(kw in title_lower for kw in ["ai", "machine", "neural", "deep", "algorithm"]):
            return "AI/ML"
        elif any(kw in title_lower for kw in ["stock", "market", "finance", "trade"]):
            return "Finance"
        elif any(kw in title_lower for kw in ["apple", "microsoft", "google", "amazon"]):
            return "Tech Giants"
        elif any(kw in title_lower for kw in ["startup", "funding", "venture"]):
            return "Startups"
        elif any(kw in title_lower for kw in ["security", "cyber", "hack"]):
            return "Security"
        else:
            return topic or "General"
