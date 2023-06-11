from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from api.v1.app.schemas import UserLogin
from api.v1.app.shortcuts import render_template, redirect_to
from api.v1.app.utils import valid_schema_data

router = APIRouter(tags=["Authentication"], prefix="/api/auth")


@router.get("/token/sign-in", response_class=HTMLResponse)
async def user_login(request: Request):
    return render_template(request, "auth/sign-in.html", {})


@router.post("/token/sign-in", response_class=HTMLResponse)
async def user_login(
        request: Request, email: str = Form(...), password: str = Form(...), _next: Optional[str] = "/"
):
    rw_data = {"email": email, "password": password}
    data, errors = valid_schema_data(UserLogin, rw_data)
    if errors:
        return render_template(request, "auth/sign-in.html", {
            "data": data,
            "errors": errors
        }, status_code=400)
    if "http://127.0.0.1" not in _next:
        _next = "/"
    return redirect_to(_next, cookies=data)


@router.get("/logout", response_class=HTMLResponse)
async def user_logout(request: Request):
    return redirect_to("/api/auth/token/sign-in", remove_session=True)
