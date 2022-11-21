"""A module to handle tokens.

This module is responsible for token responses, signing and decoding.
For more control on JWT duration, you can set JWT_SECRET with your own secret.
"""
import logging
import secrets
import time

import jwt

logger = logging.getLogger("token handler")

JWT_SECRET = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"


def token_response(token: str) -> dict[str, str]:
    """Returns a token response for a given token.

    Arguments:
        token (str): The token to be used.

    Returns:
        A dict with the access token.
    """
    return {"access_token": token}


def sign_jwt(user_id: str) -> dict[str, str]:
    """Sign a paylod and return the signed token.

    Arguments:
        user_id (str): The user idi used to login.

    Returns:
        A token with the signed payload.
    """
    payload = {"user_id": user_id, "expires": time.time() + 86400}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict[str, str]:
    """Decode the token.

    Arguments:
        token (str): The token to be decodded.

    Returns:
        The decoded token if possible to decode, or else an empty dict.
    """
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
