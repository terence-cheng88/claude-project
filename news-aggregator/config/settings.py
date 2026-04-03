"""
Configuration settings using Pydantic
"""

from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Ruflo News Aggregator"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Debug mode")

    # News sources
    max_articles: int = Field(default=20, ge=1, le=100)
    default_time_range: str = Field(default="24h", choices=["1h", "6h", "24h", "7d"])

    # News API (optional)
    news_api_key: Optional[str] = Field(
        default=None,
        description="NewsAPI key (optional - use RSS feeds if not set)"
    )

    # Redis (optional - for production)
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis URL for caching"
    )

    # Logging
    log_level: str = Field(default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        description="Comma-separated CORS origins"
    )

    # Health check
    health_check_interval: int = Field(default=30, ge=5, le=300)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


def get_settings() -> Settings:
    """Get settings instance"""
    return Settings()
