"""Repository for Lead database operations."""
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
import logging

from app.models.lead import Lead
from app.config import settings

logger = logging.getLogger(__name__)


class LeadRepository:
    """Repository class for Lead database operations."""

    def __init__(self):
        """Initialize the Lead repository."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.collection_name = "leads"

    async def connect(self):
        """Connect to MongoDB database."""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            self.database = self.client[settings.mongodb_db_name]
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    async def disconnect(self):
        """Disconnect from MongoDB database."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    async def create(self, lead: Lead) -> Lead:
        """
        Create a new lead in the database.

        Args:
            lead: Lead instance to create

        Returns:
            Created Lead instance with generated ID

        Raises:
            Exception: If database operation fails
        """
        try:
            collection = self.database[self.collection_name]
            lead_dict = {
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "birth_date": lead.birth_date,
            }

            result = await collection.insert_one(lead_dict)
            lead.id = str(result.inserted_id)

            logger.info(f"Created lead with ID: {lead.id}")
            return lead

        except Exception as e:
            logger.error(f"Failed to create lead: {str(e)}")
            raise

    async def get_by_id(self, lead_id: str) -> Optional[Lead]:
        """
        Get a lead by its ID.

        Args:
            lead_id: Lead's unique identifier

        Returns:
            Lead instance if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            if not ObjectId.is_valid(lead_id):
                logger.warning(f"Invalid ObjectId format: {lead_id}")
                return None

            collection = self.database[self.collection_name]
            lead_data = await collection.find_one({"_id": ObjectId(lead_id)})

            if lead_data:
                return Lead.from_dict(lead_data)

            logger.info(f"Lead not found with ID: {lead_id}")
            return None

        except Exception as e:
            logger.error(f"Failed to get lead by ID: {str(e)}")
            raise

    async def get_all(self) -> List[Lead]:
        """
        Get all leads from the database.

        Returns:
            List of Lead instances

        Raises:
            Exception: If database operation fails
        """
        try:
            collection = self.database[self.collection_name]
            leads_data = await collection.find().to_list(length=None)

            leads = [Lead.from_dict(lead_data) for lead_data in leads_data]

            logger.info(f"Retrieved {len(leads)} leads from database")
            return leads

        except Exception as e:
            logger.error(f"Failed to get all leads: {str(e)}")
            raise

    async def exists_by_email(self, email: str) -> bool:
        """
        Check if a lead with the given email already exists.

        Args:
            email: Email address to check

        Returns:
            True if lead exists, False otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            collection = self.database[self.collection_name]
            count = await collection.count_documents({"email": email})
            return count > 0

        except Exception as e:
            logger.error(f"Failed to check if lead exists: {str(e)}")
            raise


# Singleton instance
lead_repository = LeadRepository()
