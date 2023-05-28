"""
This module provides functions for rendering templates and performing redirects in the FastAPI application.

Functions:
- render_template: Renders a template with the specified context and returns an HTML response.
- redirect_to: Creates a redirect response to the specified URL with optional cookies and session removal.

"""


from .config import get_settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from cassandra.cqlengine.query import DoesNotExist, MultipleObjectsReturned
from fastapi import Request

settings = get_settings()

templates = Jinja2Templates(directory=str(settings.template_dir))


def render_template(
    request, template_name: str, context: dict, status_code: int = 200, cookies: dict = None
):
    """
    Render a template with the specified context and return an HTML response.

    Args:
        request: The FastAPI request object.
        template_name: The name of the template to render.
        context: A dictionary containing the context data for the template.
        status_code: The HTTP status code for the response (default: 200).
        cookies: Optional dictionary containing cookies to be set in the response.

    Returns:
        An HTMLResponse containing the rendered template.

    """
    ctx_copy = context.copy()
    ctx_copy.update({"request": request})

    html_string = templates.get_template(template_name).render(ctx_copy)
    response = HTMLResponse(html_string, status_code=status_code)

    if cookies:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True, secure=True, samesite="strict")

    return response


def redirect_to(url: str, cookies: dict = None, remove_session: bool = False):
    """
    Create a redirect response to the specified URL with optional cookies and session removal.

    Args:
        url: The URL to redirect to.
        cookies: Optional dictionary containing cookies to be set in the response.
        remove_session: Boolean indicating whether to remove the session cookies (default: False).

    Returns:
        A RedirectResponse to the specified URL.

    """
    response = RedirectResponse(url, status_code=302)

    if cookies:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True, secure=True, samesite="strict")

    if remove_session:
        response.set_cookie(key="session_ended", value=1, httponly=True, secure=True, samesite="strict")
        response.delete_cookie("session_id")

    return response


def found_object_or_404(ClassName, **kwargs):
    """
    Retrieve an object of the specified class using the provided kwargs or return None if not found.

    Args:
        ClassName: The class of the object to retrieve.
        **kwargs: Keyword arguments for filtering the objects.

    Returns:
        An object of the specified class if found, otherwise None.

    """
    try:
        obj = ClassName.objects.get(**kwargs)
    except DoesNotExist:
        raise StarletteHTTPException(status_code=404)
    except MultipleObjectsReturned:
        raise StarletteHTTPException(status_code=400)
    except Exception as e:
        raise StarletteHTTPException(status_code=500)
    return obj


def is_htmx(request: Request):
    return request.headers.get("hx-request") == "true"
