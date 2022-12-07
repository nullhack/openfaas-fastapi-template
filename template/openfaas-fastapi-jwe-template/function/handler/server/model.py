"""This module defines models used by FastAPI."""
from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    """Define a request model."""

    data: dict


class ResponseModel(BaseModel):
    """Define a response model."""

    data: dict


class UserLoginSchema(BaseModel):
    """Define a user login schema."""

    user_id: str = Field(...)
    password: str = Field(...)

    class Config:
        """Configure extra configurations to show default example of login."""

        schema_extra = {
            "example": {"user_id": "user_id", "password": "password"}
        }
