"""This module defines models used by fastapi."""
from typing import Dict

from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    """Define a request model."""

    data: Dict


class ResponseModel(BaseModel):
    """Define a response model."""

    data: Dict


class UserLoginSchema(BaseModel):
    """Define a user login schema."""

    user_id: str = Field(...)
    password: str = Field(...)

    class Config:
        """Configure extra configurations to show default example of login."""

        schema_extra = {
            "example": {"user_id": "user_id", "password": "password"}
        }
