"""Feature steps implementation.

Source file: handler.feature
"""
from pytest_bdd import given, scenario, scenarios, then

from handler import handler

scenario("handler.feature", "Basic output")


@given("an input to the handler", target_fixture="handler_out")
def _() -> dict:
    """An input to the handler.

    Returns:
        The output of handle.
    """
    return handler.handle({})


@then("the output of the handler must be of type dict")
def _(handler_out: dict) -> None:
    """The output of the handler must be of type dict.

    Arguments:
        handler_out (dict): fixture containing the output of handler.
    """
    assert isinstance(handler_out, dict)


scenarios("handler.feature")
