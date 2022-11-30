"""Defines how the API will handle requests."""
import json
import os

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from starlette import status
from starlette.responses import HTMLResponse

from .. import handler
from .auth.auth_bearer import JWEBearer
from .auth.auth_handler import decrypt_jwe, encrypt_jwe
from .model import RequestModel, ResponseModel, UserLoginSchema
from .utils.swagger import get_swagger_ui_html

func_name = os.getenv("FUNCNAME", "")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    servers=[
        {"url": "/"},
        {"url": f"/function/{func_name}"},
    ],
)

body = Body()


@app.get(
    "/docs",
    response_class=HTMLResponse,
    description="Swagger UI HTML.",
    include_in_schema=False,
)
async def swagger_ui_html() -> HTMLResponse:
    """Returns a swagger html.

    Returns:
        A HTMLResponse containing the UI specified in the OpenAPI specification.
    """
    openapi_html = get_swagger_ui_html(
        openapi_spec=json.dumps(app.openapi()),
        title=f"OpenFaas function: {func_name}",
    )
    return openapi_html


@app.post("/auth", tags=["Auth"], description="User login.")
async def user_login(user: UserLoginSchema = body) -> dict:
    """Returns a JWE if the user is authenticated.

    Arguments:
        user (UserLoginSchema): User login object.

    Returns:
        A JWE response signed.

    Raises:
        HTTPException: If user fails to authenticate.
    """
    jwe_response = {}
    if handler.check_auth(user):
        jwe_response = encrypt_jwe(iss=func_name)
    else:
        raise HTTPException(status_code=403, detail="Wrong credentials")
    return jwe_response


@app.get("/", tags=["Request"], description="Read root.")
async def read_root(request: Request) -> dict:
    """Defines actions to be taken when a get request is made to the root page.

    Arguments:
        request (Request): User request object.

    Returns:
        Dictionary containing the request parameters.
    """
    return {"params": request.query_params}


@app.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Handle the request.",
    response_model=ResponseModel,
    tags=["Request"],
    dependencies=[Depends(JWEBearer())],
)
async def handle_request(
    *,
    req_model: RequestModel,
    request: Request,
) -> dict:
    """Defines actions to be taken when a post request is made to the root page.

    Arguments:
        req_model (RequestModel): User request object.
        request (Request): FastAPI request object.

    Returns:
        Dictionary containing the response.

    Raises:
        HTTPException: When the handler raises any Exception.
    """
    try:
        token = await JWEBearer()(request)
        auth_token = decrypt_jwe(token)
        res = ResponseModel(
            data=handler.handle(req_model.data, auth_token=auth_token)
        )
    except Exception:
        raise HTTPException(status_code=500, detail="An API Error occurred")
    return res


def run() -> None:
    """Run the server."""
    import uvicorn

    uvicorn.run(
        "handler.server.api:app", host="127.0.0.1", port=8000, reload=True
    )


if __name__ == "__main__":
    run()
