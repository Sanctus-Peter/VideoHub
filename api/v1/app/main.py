from typing import Optional

from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.responses import HTMLResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
from api.v1.app.shortcuts import render_template, redirect_to, is_htmx
from api.v1.app.search_client import update_index, search_index

from . import database, shortcuts, oauth2
from .exceptions import HandleExceptions
from .models import User, Video, WatchEvent, Playlist
from .routers import users, auth, videos, watch_event, playlist

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
    response = redirect_to(f"/api/auth/token/sign-in?next={request.url}", remove_session=True)
    if is_htmx(request):
        response.status_code = 200
        response.headers['HX-Redirect'] = "/api/auth/token/sign-in"
    return response


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
    sync_table(Video)
    sync_table(WatchEvent)
    sync_table(Playlist)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(watch_event.router)
app.include_router(playlist.router)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    if request.user.is_authenticated:
        return shortcuts.render_template(request, "dashboard.html", {})
    return shortcuts.render_template(request, "home.html", {})


@app.get("/api/search", response_class=HTMLResponse)
def search_for_content(request: Request, q: Optional[str] = None):
    qry = None
    context = {}
    if q:
        qry = q
        results = search_index(qry)
        context = {
            "hits": results.get("hits"),
            "num_hits": results.get("nbHits"),
            "query": qry
        }
    return render_template(request, "search/details.html", context)


@app.post("/api/update-index", response_class=HTMLResponse)
def update_search_index(request: Request):
    count = update_index()
    return HTMLResponse(f"{count} Refreshed")
