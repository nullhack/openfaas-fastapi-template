"""This module defines how requests are handled by the server."""


def handle(req: dict, auth_token: str = "") -> dict:  # noqa: S107
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.
        auth_token (str): The token used to authenticate.

    Returns:
        A dictionary containing the results for the request.
    """
    return {"token": auth_token}
