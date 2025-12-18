"""Pydantic schemas for Lead validation and serialization."""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class LeadCreateSchema(BaseModel):
    """Schema for creating a new lead."""

    name: str = Field(..., min_length=1, max_length=200, description="Lead's full name")
    email: EmailStr = Field(..., description="Lead's email address")
    phone: str = Field(..., min_length=1, max_length=20, description="Lead's phone number")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890"
            }
        }
    )


class LeadResponseSchema(BaseModel):
    """Schema for lead response."""

    id: str = Field(..., description="Lead's unique identifier")
    name: str = Field(..., description="Lead's full name")
    email: str = Field(..., description="Lead's email address")
    phone: str = Field(..., description="Lead's phone number")
    birth_date: Optional[str] = Field(None, description="Lead's birth date (YYYY-MM-DD format)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "birth_date": "1998-02-05"
            }
        }
    )


class LeadListResponseSchema(BaseModel):
    """Schema for list of leads response."""

    leads: list[LeadResponseSchema] = Field(..., description="List of leads")
    total: int = Field(..., description="Total number of leads")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "leads": [
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone": "+1234567890",
                        "birth_date": "1998-02-05"
                    }
                ],
                "total": 1
            }
        }
    )
