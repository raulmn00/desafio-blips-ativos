"""Application configuration module."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # MongoDB Configuration
    mongodb_url: str = "mongodb://admin:admin123@localhost:27017"
    mongodb_db_name: str = "leads_db"

    # External API Configuration
    external_api_url: str = "https://dummyjson.com"
    external_api_timeout: int = 10  # seconds

    # Application Configuration
    app_title: str = "Leads Management API"
    app_version: str = "1.0.0"
    app_description: str = "API for managing leads with external API integration"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
