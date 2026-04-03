"""
Pytest configuration and fixtures
"""

import pytest

# pytest-asyncio for async tests
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def test_topic():
    """Common test topic"""
    return "ai"


@pytest.fixture(scope="session")
def test_max_articles():
    """Common max articles value"""
    return 10


@pytest.fixture(scope="session")
def test_sources():
    """Common sources setting"""
    return "rss"
