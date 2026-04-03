"""
Application error handling
"""

from fastapi import HTTPException, status
from typing import Optional


class AppError(Exception):
    """Base application exception"""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NewsNotFoundError(AppError):
    """News article not found"""

    def __init__(self, news_id: str):
        super().__init__(
            message=f"News article not found: {news_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )


class RateLimitExceeded(AppError):
    """Rate limit exceeded"""

    def __init__(self, limit: int, retry_after: int):
        super().__init__(
            message=f"Rate limit exceeded. Retry after {retry_after} seconds",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"limit": limit, "retry_after": retry_after}
        )


class InvalidTopic(AppError):
    """Invalid topic provided"""

    def __init__(self, topic: str):
        super().__init__(
            message=f"Invalid topic: '{topic}' is not recognized",
            status_code=status.HTTP_400_BAD_REQUEST
        )
