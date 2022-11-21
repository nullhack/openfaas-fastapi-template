"""A module to bear JWT tokens.

This module is responsible for defining a JWT beared classs to be used in fastapi.
"""
from typing import TypeVar

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decode_jwt

Self = TypeVar("Self", bound="JWTBearer")


class JWTBearer(HTTPBearer):
    """A class to define a JWT Token Bearer."""

    def __init__(self: Self, auto_error: bool = True) -> None:
        """Initialize JWTBearer instances.

        Arguments:
            auto_error (bool): define auto error for HTTPBearer. Default `True`.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self: Self, request: Request) -> str:
        """Define behaviour when the class is called.

        Arguments:
            request (Request): The request to be checked.

        Returns:
            A credential if it's valid.

        Raises:
            HTTPException: If there's any issue with the credentials.
        """
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        checked_credentials = ""

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            checked_credentials = credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

        return checked_credentials

    def verify_jwt(self: Self, jwt_token: str) -> bool:
        """Verify a JWT token.

        Arguments:
            jwt_token (str): JWT token to be verified.

        Returns:
            A boolean showing if the token is valid or not.
        """
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except Exception:
            payload = {}
        if payload:
            is_token_valid = True
        return is_token_valid
