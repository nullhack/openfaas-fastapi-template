"""This module defines how requests are handled by the server."""


def handle(req: dict, auth_token: dict = None) -> dict:  # noqa: S107
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.
        auth_token (dict): The token information used to authenticate.

    Returns:
        A dictionary containing the results for the request.
    """
    return {"req": req, "auth_token": auth_token}
