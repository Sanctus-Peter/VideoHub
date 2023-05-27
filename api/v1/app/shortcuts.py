from .config import get_settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

settings = get_settings()

templates = Jinja2Templates(directory=str(settings.template_dir))


def render_template(
        request, template_name: str, context: dict, status_code: int = 200, cookies: dict = None
):
    ctx_copy = context.copy()
    ctx_copy.update({"request": request})

    html_string = templates.get_template(template_name).render(ctx_copy)
    response = HTMLResponse(html_string, status_code=status_code)

    if cookies:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True, secure=True, samesite="strict")
    # return templates.TemplateResponse(template_name, ctx_copy, status_code=status_code)
    return response


def redirect_to(url: str, cookies: dict = None, remove_session: bool = False):
    response = RedirectResponse(url, status_code=302)
    if cookies:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True, secure=True, samesite="strict")
    if remove_session:
        response.set_cookie(key="session_ended", value=1, httponly=True, secure=True, samesite="strict")
        response.delete_cookie("session_id")
    return response
