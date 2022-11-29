"""A module to handle tokens.

This module is responsible for token responses, signing and decoding.
For more control on JWE duration, you can set JWE_SECRET with your own secret.
"""
import json
import logging
import secrets
import time

from jose import jwe

logger = logging.getLogger("token handler")

# If you need control over the encryption password, change the line below
JWE_SECRET = secrets.token_urlsafe(24)
JWE_ALGORITHM = "A256KW"
JWE_ENCRYPTION = "A256GCM"


def token_response(token: str) -> dict[str, str]:
    """Returns a token response for a given token.

    Arguments:
        token (str): The token to be used.

    Returns:
        A dict with the access token.
    """
    return {"access_token": token}


def encrypt_jwe(user_id: str) -> dict[str, str]:
    """Sign a paylod and return the signed token.

    Arguments:
        user_id (str): The user idi used to login.

    Returns:
        A token with the signed payload.
    """
    t = time.time()
    payload = json.dumps({"iat": t, "exp": t + 86400})
    token = jwe.encrypt(
        payload, JWE_SECRET.encode(), algorithm=JWE_ALGORITHM, encryption=JWE_ENCRYPTION
    )

    return token_response(token)


def decrypt_jwe(token: str) -> dict[str, str]:
    """Decode the token.

    Arguments:
        token (str): The token to be decodded.

    Returns:
        The decoded token if possible to decode, or else an empty dict.
    """
    decoded_token = json.loads(jwe.decrypt(token, JWE_SECRET.encode()))
    return decoded_token if decoded_token["exp"] >= time.time() else {}
