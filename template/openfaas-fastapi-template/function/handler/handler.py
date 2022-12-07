"""This module defines how requests are handled by the server."""


def handle(req: dict) -> dict:
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.

    Returns:
        A dictionary containing the results for the request.
    """
    return {"req": req}
