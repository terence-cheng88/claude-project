"""
Tests for News Feeder Agent
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.feeder import NewsFeederAgent


@pytest.fixture
def feeder_agent():
    """Create a feeder agent for testing"""
    return NewsFeederAgent("test-request-1", 0)


def test_feeder_initialization(feeder_agent):
    """Test that feeder agent initializes correctly"""
    assert feeder_agent.request_id == "test-request-1"
    assert feeder_agent.index == 0
    assert feeder_agent.name == "Feeder-0"


def test_feeder_fetch_articles(feeder_agent):
    """Test feeder fetch functionality"""
    result = feeder_agent.fetch_articles("tech", max_articles=5)
    assert "status" in result
    assert "articles" in result
    # RSS feed should return some articles
    assert len(result.get("articles", [])) > 0


def test_feeder_empty_result(feeder_agent):
    """Test handling of empty results"""
    result = feeder_agent.fetch_articles("nonexistent-topic-12345", max_articles=1)
    assert "status" in result
    # May still have articles due to RSS fallback
