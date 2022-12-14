"""Defines how the API will handle requests."""
import json
import os

from fastapi import Body, FastAPI, HTTPException, Request
from starlette import status
from starlette.responses import HTMLResponse

from .. import handler
from .model import RequestModel, ResponseModel
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


@app.get("/", tags=["Request"], description="Read root.")
@app.post("/", tags=["Request"], description="Read root.")
async def read_root(request: Request) -> dict:
    """Defines actions to be taken when a get request is made to the root page.

    Arguments:
        request (Request): User request object.

    Returns:
        Dictionary containing the request parameters.
    """
    return {"params": request.query_params}


@app.post(
    "/handle",
    status_code=status.HTTP_200_OK,
    description="Handle the request.",
    response_model=ResponseModel,
    tags=["Request"],
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
        res = ResponseModel(data=handler.handle(req_model.data))
    except Exception:  # pragma: no cover
        # This line is to ensure that any unexpected error will be captured
        # Testing this behavior would introduce hacks in handle, which is not good
        raise HTTPException(status_code=500, detail="An API Error occurred")
    return res


def run() -> None:  # pragma: no cover
    """Run the server."""
    import uvicorn

    uvicorn.run(
        "handler.server.api:app", host="127.0.0.1", port=8000, reload=True
    )


if __name__ == "__main__":
    run()
