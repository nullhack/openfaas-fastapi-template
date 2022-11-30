"""This module defines how requests are handled by the server."""
from .server.model import UserLoginSchema


def check_auth(login_data: UserLoginSchema) -> bool:
    """Checks the user login.

    Arguments:
        login_data (UserLoginSchema): User login data.

    Returns:
        True if the login is correct and False if it is not.
    """
    # To improve authentication rules change the line below!
    check = bool(login_data.user_id and login_data.password)
    return check


def handle(req: dict, auth_token: dict = None) -> dict:
    """Handle a request to the function.

    Args:
        req (dict): The request parameters.
        auth_token (dict): The token information used to authenticate.

    Returns:
        A dictionary containing the results for the request.
    """
    return {"req": req, "auth_token": auth_token}
