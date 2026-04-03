"""
Content Processor Agent - Extracts entities and classifies content
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from utils.news_sources import RSS_SOURCES


class ContentProcessorAgent:
    """
    Processes news articles by extracting entities and classifying content.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.name = "Processor"

    async def process(self, articles: List[dict]) -> List[dict]:
        """Process multiple articles"""
        print(f"[{self.name}] Processing {len(articles)} articles...")

        processed = []
        for article in articles:
            # Skip empty articles
            if not article.get("title"):
                continue

            processed_article = await self._process_single(article)
            processed.append(processed_article)

        print(f"[{self.name}] Processed {len(processed)} articles")
        return processed

    async def _process_single(self, article: dict) -> dict:
        """Process a single article"""
        title = article.get("title", "")
        summary = article.get("summary", "")

        # Extract entities (simple keyword-based extraction)
        entities = await self._extract_entities(title, summary)

        # Classify content
        category = await self._classify_content(title, summary)

        # Check for spam/fake signals
        is_spam = await self._detect_spam(title, summary)

        return {
            **article,
            "entities": entities,
            "category": category,
            "is_spam": is_spam,
            "keywords": self._extract_keywords(title, summary)
        }

    async def _extract_entities(self, title: str, summary: str) -> List[str]:
        """Extract key entities (companies, people, topics)"""
        text = f"{title} {summary}".lower()

        # Common entity keywords
        entities = []

        # Companies
        companies = {
            "apple": "Apple Inc.", "microsoft": "Microsoft", "google": "Google",
            "amazon": "Amazon", "meta": "Meta", "tesla": "Tesla", "nvidia": "NVIDIA"
        }
        entities.extend([v for k, v in companies.items() if k in text])

        # Topics
        topics = ["artificial intelligence", "machine learning", "climate change",
                  "cryptocurrency", "semiconductors", "cybersecurity"]
        for topic in topics:
            if topic in text or topic.replace(" ", "-") in text:
                entities.append(topic)

        # People (basic extraction)
        people_keywords = ["elon musk", "jeff bezos", "bill gates", "sam altman"]
        for person in people_keywords:
            if person in text:
                entities.append(person)

        return list(set(entities)) if entities else []

    async def _classify_content(self, title: str, summary: str) -> str:
        """Classify article content"""
        text = f"{title} {summary}".lower()

        # Tech subcategories
        if any(kw in text for kw in ["ai", "machine", "neural", "llm", "transformer"]):
            return "AI/Machine Learning"
        elif any(kw in text for kw in ["semiconductor", "chip", "cpu", "gpu"]):
            return "Semiconductors"
        elif any(kw in text for kw in ["crypto", "bitcoin", "ethereum", "blockchain"]):
            return "Cryptocurrency"
        elif any(kw in text for kw in ["startup", "unicorn", "funding"]):
            return "Venture Capital"
        else:
            return "General Tech"

    async def _detect_spam(self, title: str, summary: str) -> bool:
        """Detect spam/fake news signals"""
        text = f"{title} {summary}".lower()

        # Common spam indicators
        spam_indicators = ["click here", "buy now", "free money", "lottery",
                          "instant", "guaranteed", "winner"]
        if any(ind in text for ind in spam_indicators):
            return True

        # Suspicious URL patterns
        article_url = article.get("url", "")
        if any(ind in article_url.lower() for ind in ["suspicious", "sweepstakes"]):
            return True

        return False

    def _extract_keywords(self, title: str, summary: str) -> List[str]:
        """Extract simple keywords from title and summary"""
        text = f"{title} {summary}".lower()
        words = text.split()

        # Filter short words and common stop words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on",
                      "at", "to", "for", "of", "with", "and", "or", "but"}

        keywords = [w for w in words if len(w) > 4 and w.lower() not in stop_words]
        return list(set(keywords[:10]))
