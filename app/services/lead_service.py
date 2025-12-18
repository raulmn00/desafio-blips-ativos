"""Business logic service for Lead operations."""
from typing import List, Optional
import logging

from app.models.lead import Lead
from app.repositories.lead_repository import lead_repository
from app.services.external_api_service import external_api_service
from app.schemas.lead import LeadCreateSchema, LeadResponseSchema, LeadListResponseSchema

logger = logging.getLogger(__name__)


class LeadService:
    """Service class containing business logic for Lead operations."""

    def __init__(self):
        """Initialize the Lead service."""
        self.repository = lead_repository
        self.external_api = external_api_service

    async def create_lead(self, lead_data: LeadCreateSchema) -> LeadResponseSchema:
        """
        Create a new lead with birth date from external API.

        Args:
            lead_data: Lead creation data

        Returns:
            Created lead response

        Raises:
            ValueError: If lead with same email already exists
            Exception: If database operation fails
        """
        # Check if lead with same email already exists
        if await self.repository.exists_by_email(lead_data.email):
            logger.warning(f"Attempt to create lead with existing email: {lead_data.email}")
            raise ValueError(f"Lead with email {lead_data.email} already exists")

        # Fetch birth date from external API
        birth_date = await self.external_api.fetch_birth_date()

        if birth_date:
            logger.info(f"Birth date fetched successfully: {birth_date}")
        else:
            logger.warning("Failed to fetch birth date from external API, setting to null")

        # Create lead instance
        lead = Lead(
            name=lead_data.name,
            email=lead_data.email,
            phone=lead_data.phone,
            birth_date=birth_date,
        )

        # Save to database
        created_lead = await self.repository.create(lead)

        # Convert to response schema
        return LeadResponseSchema(
            id=created_lead.id,
            name=created_lead.name,
            email=created_lead.email,
            phone=created_lead.phone,
            birth_date=created_lead.birth_date,
        )

    async def get_lead_by_id(self, lead_id: str) -> Optional[LeadResponseSchema]:
        """
        Get a lead by its ID.

        Args:
            lead_id: Lead's unique identifier

        Returns:
            Lead response if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        lead = await self.repository.get_by_id(lead_id)

        if not lead:
            return None

        return LeadResponseSchema(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            birth_date=lead.birth_date,
        )

    async def get_all_leads(self) -> LeadListResponseSchema:
        """
        Get all leads from the database.

        Returns:
            List of all leads with total count

        Raises:
            Exception: If database operation fails
        """
        leads = await self.repository.get_all()

        lead_responses = [
            LeadResponseSchema(
                id=lead.id,
                name=lead.name,
                email=lead.email,
                phone=lead.phone,
                birth_date=lead.birth_date,
            )
            for lead in leads
        ]

        return LeadListResponseSchema(
            leads=lead_responses,
            total=len(lead_responses),
        )


# Singleton instance
lead_service = LeadService()
