"""
Tests for Content Processor Agent
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.processor import ContentProcessorAgent


@pytest.fixture
def processor_agent():
    """Create a processor agent for testing"""
    return ContentProcessorAgent("test-request-1")


@pytest.mark.asyncio
async def test_processor_initialization(processor_agent):
    """Test that processor agent initializes correctly"""
    assert processor_agent.request_id == "test-request-1"
    assert processor_agent.name == "Processor"


@pytest.mark.asyncio
async def test_processor_process_articles(processor_agent):
    """Test processing multiple articles"""
    sample_articles = [
        {
            "id": "test-1",
            "title": "AI Breakthrough in LLMs",
            "summary": "New research shows significant improvements in language models"
        }
    ]
    result = await processor_agent.process(sample_articles)
    assert len(result) == 1
    assert "entities" in result[0]
    assert "category" in result[0]


@pytest.mark.asyncio
async def test_processor_empty_articles(processor_agent):
    """Test processing empty list"""
    result = await processor_agent.process([])
    assert result == []
