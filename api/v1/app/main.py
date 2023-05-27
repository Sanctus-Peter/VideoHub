from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.responses import HTMLResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
from api.v1.app.shortcuts import render_template, redirect_to

from . import database, shortcuts, oauth2
from .exceptions import HandleExceptions
from .models import User
from .routers import users, auth


DB_SESSION = None


app = FastAPI()

origins = ["*"]

app.add_middleware(
    AuthenticationMiddleware,
    backend=oauth2.JWTCookiePayload(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HandleExceptions)
async def handle_exception_handler(request, exc):
    return redirect_to(f"/auth/token/sign-in?next={request.url}", remove_session=True)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "errors/main.html"
    context = {"status_code": status_code}
    return render_template(request, template_name, context, status_code=status_code)


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = database.get_session()
    database.get_session()
    sync_table(User)


app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    if request.user.is_authenticated:
        return shortcuts.render_template(request, "dashboard.html", {})
    return shortcuts.render_template(request, "home.html", {})
