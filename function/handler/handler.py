"""This module defines how requests are handled by the server."""
import os

FUNCTION_NAME = ""
FUNCTION_VERSION = "1.0.0"
FUNCTION_SUMMARY = "A function that does this"
FUNCTION_RESPONSE_DESC = "Definition of object returned by function"


def handle(req: dict) -> dict:
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.

    Returns:
        A dictionary containing the results for the request.
    """
    return os.environ
