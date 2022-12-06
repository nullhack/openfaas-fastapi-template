"""Feature steps implementation.

Source file: auth.feature
"""
from pytest_bdd import given, parsers, scenario, scenarios, then

from handler import handler
from handler.server.model import UserLoginSchema

scenario("auth.feature", "An empty credential should always fail")


@given(
    parsers.parse("I input a blank {user_id} or a blank {password}"),
    target_fixture="auth_out",
)
def _(user_id: str, password: str) -> bool:
    """I input a blank <user_id> or a blank <password>.

    Arguments:
        user_id (str): User id used to login
        password (str): Password used to login

    Returns:
        Boolean indicating if the login has failed or not.
    """
    login = UserLoginSchema(user_id=user_id, password=password)
    return handler.check_auth(login)


@then("check_auth should fail")
def _(auth_out: bool) -> None:
    """Check_auth should fail.

    Arguments:
        auth_out (bool): Indicate if login failed or not.
    """
    assert auth_out


scenarios("auth.feature")
