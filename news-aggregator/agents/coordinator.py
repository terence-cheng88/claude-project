"""
Swarm Coordinator - Orchestrates the multi-agent news aggregation workflow
"""

import asyncio
import uuid
from datetime import datetime
from typing import Callable
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.news_sources import RSS_SOURCES, DEFAULTS


class SwarmCoordinator:
    """
    Multi-agent swarm coordinator for news aggregation.
    Spawns feeder agents, distributes tasks, aggregates results.
    """

    def __init__(self, request_id: str = None):
        self.request_id = request_id or str(uuid.uuid4())[:8]
        self.topic: str = ""
        self.results: dict = {}
        self.status = "idle"
        self.started_at: datetime = None
        self.completed_at: datetime = None
        self.agents = {}
        self.callbacks = {
            "on_feeding": [],
            "on_processing": [],
            "on_summarization": [],
            "on_finalization": []
        }

    async def spawn_agents(self):
        """Spawn all agent instances for this swarm"""
        print(f"[COORDINATOR] Spawning agents for request {self.request_id}...")
        self.agents = {
            "coordinator": self,
            "feeders": [NewsFeederAgent(self.request_id, idx) for idx in range(3)],
            "processor": ContentProcessorAgent(self.request_id),
            "sentiment": SentimentAnalysisAgent(self.request_id),
            "summarizer": SummarizationAgent(self.request_id),
            "publisher": PublisherAgent(self.request_id)
        }
        print(f"[COORDINATOR] {len(self.agents)} agents spawned")

    async def feed_news(self):
        """Feeder agents fetch from multiple news sources"""
        print(f"[COORDINATOR] Starting news feeders...")
        self.status = "feeding"

        feed_results = []
        for feeder in self.agents["feeders"]:
            result = await feeder.fetch_articles(self.topic)
            feed_results.append(result)
            self.callbacks["on_feeding"].append(result)
            print(f"[COORDINATOR] Feeder completed: {len(result.get('articles', []))} articles")

        self.results["feed_results"] = feed_results
        return feed_results

    async def process_content(self, articles):
        """Processor agent extracts entities and classifies content"""
        print(f"[COORDINATOR] Starting content processor...")
        self.status = "processing"

        processed = await self.agents["processor"].process(articles)
        self.results["processed_articles"] = processed
        self.callbacks["on_processing"].append(processed)
        return processed

    async def analyze_sentiment(self):
        """Sentiment agent analyzes article sentiment"""
        print(f"[COORDINATOR] Starting sentiment analysis...")
        self.status = "analyzing_sentiment"

        sentiment_results = await self.agents["sentiment"].analyze(self.results["processed_articles"])
        self.results["sentiment"] = sentiment_results
        self.callbacks["on_summarization"].append(sentiment_results)
        return sentiment_results

    async def summarize(self):
        """Summarizer agent creates TL;DR for each article"""
        print(f"[COORDINATOR] Starting summarization...")
        self.status = "summarizing"

        summaries = await self.agents["summarizer"].summarize(
            self.results["processed_articles"],
            self.results["sentiment"]
        )
        self.results["summaries"] = summaries
        self.callbacks["on_summarization"].append(summaries)
        return summaries

    async def publish(self):
        """Publisher agent formats and pushes results"""
        print(f"[COORDINATOR] Starting publisher...")
        self.status = "publishing"

        final_result = self.agents["publisher"].publish(self.results)
        self.results["final_result"] = final_result
        self.completed_at = datetime.now()
        self.callbacks["on_finalization"].append(final_result)
        return final_result

    async def run(self, topic: str):
        """Run the full multi-agent pipeline"""
        self.topic = topic
        self.started_at = datetime.now()
        self.status = "running"

        print(f"\n{'='*60}")
        print(f"NEWS AGGREGATOR SWARM ACTIVATED")
        print(f"Request ID: {self.request_id}")
        print(f"Topic: {topic}")
        print(f"{'='*60}\n")

        # Spawn agents
        await self.spawn_agents()

        # Execute pipeline
        await self.feed_news()
        await self.process_content(self.results["feed_results"])
        await self.analyze_sentiment()
        await self.summarize()
        await self.publish()

        print(f"\n{'='*60}")
        print(f"SWARM COMPLETED")
        print(f"Articles processed: {len(self.results['articles'])}")
        print(f"Request ID: {self.request_id}")
        print(f"{'='*60}\n")

        return self.results["final_result"]
