from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from api.v1.app.models import User
from api.v1.app.schemas import UserCreate
from api.v1.app.shortcuts import render_template, redirect_to
from api.v1.app.utils import valid_schema_data
from api.v1.app.decorators import login_required


router = APIRouter(tags=["Users"], prefix="/api/user")


@router.get("/")
async def get_all_users():
    query = User.objects.all()
    return list(query)


@router.get("/sign-up", response_class=HTMLResponse)
async def create_user(request: Request):
    return render_template(request, "auth/sign-up.html", {})
    

@router.post("/sign-up", response_class=HTMLResponse)
async def create_user(
        request: Request, email: str = Form(...),
        firstname: str = Form(...), lastname: str = Form(...),
        password: str = Form(...), confirm_password: str = Form(...)
):
    rw_data = {
        "email": email, "firstname": firstname, "lastname": lastname,
        "password": password, "confirm_password": confirm_password
    }
    data, errors = valid_schema_data(UserCreate, rw_data)
    if errors:
        return render_template(request, "auth/sign-up.html", {
            "data": data, "errors": errors
        }, status_code=400)
    password = data.pop("password")
    data.pop("confirm_password")
    data["password"] = password.get_secret_value()
    User.create_user(**data)
    return redirect_to("/api/auth/token/sign-in")


@router.get("/account", response_class=HTMLResponse)
@login_required
async def user_account(request: Request):
    context = {}
    return render_template(request, "account.html", context)
