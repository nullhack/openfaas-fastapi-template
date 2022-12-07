"""This module defines models used by FastAPI."""
from pydantic import BaseModel


class RequestModel(BaseModel):
    """Define a request model."""

    data: dict


class ResponseModel(BaseModel):
    """Define a response model."""

    data: dict
