from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from api.v1.app.schemas import UserLogin
from api.v1.app.shortcuts import render_template, redirect_to
from api.v1.app.utils import valid_schema_data

router = APIRouter(tags=["Authentication"], prefix="/api/auth")


@router.get("/token/sign-in", response_class=HTMLResponse)
async def user_login(request: Request):
    session_id = request.cookies.get("session_id") or None
    return render_template(request, "auth/sign-in.html", {"session_id": session_id is not None})


@router.post("/token/sign-in", response_class=HTMLResponse)
async def user_login(request: Request, email: str = Form(...), password: str = Form(...)):
    rw_data = {"email": email, "password": password}
    data, errors = valid_schema_data(UserLogin, rw_data)
    if errors:
        return render_template(request, "auth/sign-in.html", {
            "data": data,
            "errors": errors
        }, status_code=400)
    return redirect_to("/", cookies=data)
