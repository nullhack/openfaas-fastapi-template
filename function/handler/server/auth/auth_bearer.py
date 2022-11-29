"""A module to bear JWE tokens.

This module is responsible for defining a JWE beared classs to be used in fastapi.
"""
from typing import TypeVar

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decrypt_jwe

Self = TypeVar("Self", bound="JWEBearer")


class JWEBearer(HTTPBearer):
    """A class to define a JWE Token Bearer."""

    def __init__(self: Self, auto_error: bool = True) -> None:
        """Initialize JWEBearer instances.

        Arguments:
            auto_error (bool): define auto error for HTTPBearer. Default `True`.
        """
        super(JWEBearer, self).__init__(auto_error=auto_error)

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
            JWEBearer, self
        ).__call__(request)

        checked_credentials = ""

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwe(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            checked_credentials = credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

        return checked_credentials

    def verify_jwe(self: Self, jwe_token: str) -> bool:
        """Verify a JWE token.

        Arguments:
            jwe_token (str): JWE token to be verified.

        Returns:
            A boolean showing if the token is valid or not.
        """
        is_token_valid: bool = False

        try:
            payload = decrypt_jwe(jwe_token)
        except Exception:
            payload = {}
        is_token_valid = bool(payload)
        return is_token_valid
