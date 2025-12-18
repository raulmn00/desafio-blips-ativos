"""API routes for Lead management."""
from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.lead import LeadCreateSchema, LeadResponseSchema, LeadListResponseSchema
from app.services.lead_service import lead_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post(
    "",
    response_model=LeadResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lead",
    description="Creates a new lead with the provided information. Birth date is automatically fetched from an external API.",
)
async def create_lead(lead_data: LeadCreateSchema) -> LeadResponseSchema:
    """
    Create a new lead.

    Args:
        lead_data: Lead creation data containing name, email, and phone

    Returns:
        Created lead with birth date fetched from external API

    Raises:
        HTTPException 400: If lead with same email already exists
        HTTPException 500: If internal server error occurs
    """
    try:
        lead = await lead_service.create_lead(lead_data)
        return lead

    except ValueError as e:
        logger.warning(f"Validation error creating lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating lead",
        )


@router.get(
    "",
    response_model=LeadListResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get all leads",
    description="Retrieves all leads from the database.",
)
async def get_all_leads() -> LeadListResponseSchema:
    """
    Get all leads.

    Returns:
        List of all leads with total count

    Raises:
        HTTPException 500: If internal server error occurs
    """
    try:
        leads = await lead_service.get_all_leads()
        return leads

    except Exception as e:
        logger.error(f"Error retrieving leads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving leads",
        )


@router.get(
    "/{lead_id}",
    response_model=LeadResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a lead by ID",
    description="Retrieves a specific lead by its unique identifier.",
)
async def get_lead_by_id(lead_id: str) -> LeadResponseSchema:
    """
    Get a lead by its ID.

    Args:
        lead_id: Lead's unique identifier

    Returns:
        Lead information

    Raises:
        HTTPException 404: If lead not found
        HTTPException 500: If internal server error occurs
    """
    try:
        lead = await lead_service.get_lead_by_id(lead_id)

        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead with ID {lead_id} not found",
            )

        return lead

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving lead",
        )
