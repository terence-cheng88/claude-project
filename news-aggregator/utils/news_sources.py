"""
News sources configuration
"""

import os

# RSS Feed sources (free, no API key required)
RSS_SOURCES = [
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category": "tech"
    },
    {
        "name": "Reuters Business",
        "url": "https://www.reuters.com/business/",
        "category": "finance"
    },
    {
        "name": "Bloomberg Tech",
        "url": "https://feeds.bloomberg.com/news/technology/rss.xml",
        "category": "tech"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "category": "tech"
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "category": "tech"
    }
]

# News API key (optional - uncomment and set if you have one)
# NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Default settings
DEFAULTS = {
    "max_articles": 20,
    "time_range": "24h",  # Options: 1h, 6h, 24h, 7d
    "sources": "all",  # Options: all, rss, api
    "language": "en"
}
