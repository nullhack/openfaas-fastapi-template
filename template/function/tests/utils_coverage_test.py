"""Coverage test for util scripts."""
from starlette.responses import HTMLResponse

from handler.server.utils import swagger


def test_swagger() -> None:
    """Check if divide works for expected entries."""
    html = swagger.get_swagger_ui_html(
        openapi_spec="",
        title="",
    )
    assert isinstance(html, HTMLResponse)
