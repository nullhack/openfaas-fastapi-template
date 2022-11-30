"""This module provides scripts tto help generate swagger documentation."""
from starlette.responses import HTMLResponse


def get_swagger_ui_html(
    *,
    openapi_spec: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    swagger_favicon_url: str = "https://raw.githubusercontent.com/openfaas/docs/master/docs/images/favicon.ico",
) -> HTMLResponse:
    """A tweaked on fastapi.openapi.docs.get_swagger_ui_html to generate from raw JSON as opposed to using a url.

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
