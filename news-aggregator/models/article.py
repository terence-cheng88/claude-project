"""
Article model - represents a single news article
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Article(BaseModel):
    """Represents a single news article"""
    id: str
    title: str
    summary: str
    url: str
    published_at: datetime
    source: str
    category: Optional[str] = None
    sentiment: Optional[float] = None  # -1 to 1
    entities: Optional[list] = None  # People, companies, topics

    class Config:
        json_schema_extra = {
            "description": "A news article from any RSS or API source"
        }
