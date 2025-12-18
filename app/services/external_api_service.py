"""Service for integrating with external API."""
import httpx
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class ExternalAPIService:
    """Service to interact with external API for fetching user data."""

    def __init__(self):
        """Initialize the external API service."""
        self.base_url = settings.external_api_url
        self.timeout = settings.external_api_timeout

    async def fetch_birth_date(self) -> Optional[str]:
        """
        Fetch birth date from external API.

        Returns:
            Birth date in YYYY-MM-DD format or None if API fails

        Note:
            If the external API is unavailable or returns an error,
            this method returns None to allow lead creation to continue.
            This is a design decision to prevent external API failures
            from blocking lead creation.
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/users/1")
                response.raise_for_status()
                data = response.json()

                # Extract birth date from response
                birth_date = data.get("birthDate")

                if birth_date:
                    logger.info(f"Successfully fetched birth date from external API: {birth_date}")
                    return birth_date
                else:
                    logger.warning("External API response does not contain birth date")
                    return None

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while fetching birth date: {e.response.status_code}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error occurred while fetching birth date: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error occurred while fetching birth date: {str(e)}")
            return None


# Singleton instance
external_api_service = ExternalAPIService()
