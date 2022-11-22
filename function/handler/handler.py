"""This module defines how requests are handled by the server."""
import os

FUNCTION_NAME = ""


def handle(req: dict) -> dict:
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.

    Returns:
        A dictionary containing the results for the request.
    """
    return os.environ
