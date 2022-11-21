"""Defines how the API will handle requests."""
import json

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.responses import HTMLResponse

from .. import handler
from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import sign_jwt
from .model import RequestModel, ResponseModel, UserLoginSchema

app = FastAPI(docs_url=None, redoc_url=None)


def get_swagger_ui_html(
    *,
    openapi_spec: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    swagger_favicon_url: str = "https://raw.githubusercontent.com/openfaas/docs/master/docs/images/favicon.ico",
) -> HTMLResponse:
    """A tweaked fastapi.openapi.docs.get_swagger_ui_html to generate from raw JSON as opposed to using a url.

    Arguments:
        openapi_spec (str): OpenAPI speficication JSON encoded as string.
        title (str): Title of the page.
        swagger_js_url (str): Custom Javascript URL.
        swagger_css_url (str): Custom CSS URL.
        swagger_favicon_url (str): Custom favicon URL.

    Returns:
        HTMLResponse: Renderized documentation page as HTML.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const spec = JSON.parse(`
        {openapi_spec}
    `)
    const ui = SwaggerUIBundle({{
        spec: spec,
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true
    }})
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


def custom_openapi() -> dict:
    """Generates schema from OpenFaas function particulars.

    Returns:
        An OpenAPI schema.
    """
    openapi_schema = get_openapi(
        title=f"The Amazing Programming Language Info API - {handler.FUNCTION_NAME}",
        version=f"v{handler.FUNCTION_VERSION}",
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": f"The Amazing Programming Language Info API - {handler.FUNCTION_NAME}",
        "version": f"v{handler.FUNCTION_VERSION}",
        "description": "Learn about programming language history!",
        "termsOfService": "http://programming-languages.com/terms/",
        "contact": {
            "name": "Get Help with this API",
            "url": "http://www.programming-languages.com/help",
            "email": "support@programming-languages.com",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    }
    paths = openapi_schema["paths"]
    upd_paths = {}
    # Supplement path specs
    for key in paths:
        path = paths[key]
        rel_path = f"{handler.FUNCTION_NAME}"
        if key.startswith(rel_path):
            upd_paths[key] = path
        else:
            rel_path = f"{rel_path}{key}"
            upd_paths[rel_path] = path

    openapi_schema["paths"] = upd_paths
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get(
    "/docs",
    response_class=HTMLResponse,
    description="Swagger UI HTML.",
    summary="Function Swagger UI Doc",
    response_description="Swagger UI documentation rendered as HTML (for consumption directly in a web browser)",
    include_in_schema=False,
)
async def swagger_ui_html() -> HTMLResponse:
    """Returns a swagger html.

    Returns:
        A HTMLResponse containing the UI specified in the OpenAPI specification.
    """
    openapi_html = get_swagger_ui_html(
        openapi_spec=json.dumps(app.openapi()),
        title=f"OpenFaas function: {handler.FUNCTION_NAME.title()}",
    )
    return openapi_html


def check_auth(data: UserLoginSchema) -> bool:
    """Checks the user login.

    Arguments:
        data (UserLoginSchema): User login data.

    Returns:
        True if the login is correct and False iff it is not.
    """
    check = False
    if data.user_id and data.password:
        check = True
    return check


body = Body()


@app.post("/auth", tags=["Auth"], description="User login.")
async def user_login(user: UserLoginSchema = body) -> dict:
    """Returns a JWT if the user is authenticated.

    Arguments:
        user (UserLoginSchema): User login object.

    Returns:
        A JWT response signed.

    Raises:
        HTTPException: If user fails to authenticate.
    """
    jwt_response = {}
    if check_auth(user):
        jwt_response = sign_jwt(user.user_id)
    else:
        raise HTTPException(status_code=403, detail="Wrong credentials")
    return jwt_response


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
    response_description=handler.FUNCTION_RESPONSE_DESC,
    tags=["Request"],
    dependencies=[Depends(JWTBearer())],
)
async def handle_request(
    *,
    req: RequestModel,
) -> dict:
    """Defines actions to be taken when a post request is made to the root page.

    Arguments:
        req (RequestModel): User request object.

    Returns:
        Dictionary containing the response.

    Raises:
        HTTPException: When the handler raises any Exception.
    """
    try:
        res = ResponseModel(data=handler.handle(req.data))
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
