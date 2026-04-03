"""
Sentiment Analysis Agent - Analyzes article sentiment
"""

import sys
import os
import textblob
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SentimentAnalysisAgent:
    """
    Analyzes sentiment of news articles.
    Uses TextBlob for quick sentiment scoring.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.name = "SentimentAgent"
        self._negative_words = {
            "bad", "worst", "crash", "fail", "scandal", "lawsuit",
            "loss", "drop", "decline", "plummet", "tumble", "ruin"
        }
        self._positive_words = {
            "great", "best", "gain", "profit", "boom", "success",
            "growth", "rise", "surge", "win", "victory", "breakthrough"
        }

    async def analyze(self, articles: List[dict]) -> List[dict]:
        """Analyze sentiment for all articles"""
        print(f"[{self.name}] Analyzing sentiment for {len(articles)} articles...")

        results = []
        for article in articles:
            if not article.get("summary"):
                continue

            sentiment = await self._analyze_article(article)
            results.append({**article, **sentiment})

        # Calculate aggregate sentiment
        if results:
            avg_sentiment = sum(r["sentiment"] for r in results) / len(results)
            print(f"[{self.name}] Average sentiment: {avg_sentiment:.2f}")

        return results

    async def _analyze_article(self, article: dict) -> dict:
        """Analyze a single article's sentiment"""
        text = article.get("summary", "") or article.get("title", "")

        # Use TextBlob for sentiment analysis
        try:
            blob = textblob.TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1

            # Classify sentiment
            if polarity < -0.2:
                classification = "negative"
            elif polarity > 0.2:
                classification = "positive"
            else:
                classification = "neutral"

            return {
                "sentiment": polarity,
                "classification": classification,
                "subjectivity": subjectivity
            }
        except Exception as e:
            # Fallback to keyword-based analysis
            return self._keyword_sentiment(text)

    def _keyword_sentiment(self, text: str) -> dict:
        """Fallback sentiment analysis using keywords"""
        words = text.lower().split()
        sentiment_score = 0

        for word in words:
            word_clean = word.strip(".,!?\"'")
            if word_clean in self._positive_words:
                sentiment_score += 0.1
            elif word_clean in self._negative_words:
                sentiment_score -= 0.1

        # Normalize to -1 to 1 range
        sentiment_score = max(-1, min(1, sentiment_score))

        if sentiment_score < -0.2:
            classification = "negative"
        elif sentiment_score > 0.2:
            classification = "positive"
        else:
            classification = "neutral"

        return {
            "sentiment": sentiment_score,
            "classification": classification
        }

    def get_sentiment_distribution(self, articles: List[dict]) -> dict:
        """Get sentiment breakdown across all articles"""
        if not articles:
            return {}

        classifications = {}
        for article in articles:
            sentiment = article.get("sentiment")
            if sentiment:
                classification = "positive" if sentiment > 0 else "negative"
                classifications[classification] = classifications.get(classification, 0) + 1

        return {
            "positive": classifications.get("positive", 0),
            "negative": classifications.get("negative", 0),
            "neutral": len(articles) - sum(classifications.values())
        }
