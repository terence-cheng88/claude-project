"""
WebSocket handler for real-time news streaming
"""

import asyncio
from fastapi import WebSocket
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator import SwarmCoordinator


async def connect(websocket: WebSocket):
    """
    WebSocket endpoint for real-time news streaming.
    """
    await websocket.accept()
    print("[WebSocket] Connection established")

    try:
        # Receive initial topic
        topic_data = await websocket.receive_text()
        topic = topic_data.get("topic", "tech")
        max_articles = topic_data.get("limit", 10)

        print(f"[WebSocket] Streaming news for: {topic}")

        # Create coordinator
        coordinator = SwarmCoordinator()

        # Start pipeline and stream progress
        coordinator.topic = topic
        await coordinator.spawn_agents()

        # Stream feeding
        await coordinator.feed_news()

        # Stream processing
        await coordinator.process_content(coordinator.results.get("feed_results", []))

        # Stream sentiment analysis
        await coordinator.analyze_sentiment()

        # Stream summarization
        await coordinator.summarize()

        # Stream final results
        result = coordinator.results.get("final_result", {})
        articles = result.get("articles", [])

        for article in articles:
            await websocket.send_json({
                "type": "article",
                "title": article.get("title", ""),
                "summary": article.get("summary", "")[:200],
                "source": article.get("source", ""),
                "sentiment": article.get("sentiment")
            })

        # Send completion
        await websocket.send_json({
            "type": "complete",
            "total": len(articles)
        })

    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass
    finally:
        await websocket.close()
