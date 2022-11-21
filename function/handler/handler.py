FUNCTION_NAME = ""
FUNCTION_VERSION = "1.0.0"
FUNCTION_SUMMARY = "A function that does this"
FUNCTION_RESPONSE_DESC = "Definition of object returned by function"

import os


def handle(req):
    """handle a request to the function
    Args:
        req (dict): request body
    """
    return os.environ
