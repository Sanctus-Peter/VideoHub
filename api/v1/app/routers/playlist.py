import uuid
from typing import Optional

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.v1.app import utils
from api.v1.app.models import Playlist, WatchEvent
from api.v1.app.schemas import PlaylistCreate, PlaylistVideoCreate
from api.v1.app.decorators import login_required
from api.v1.app.shortcuts import (
    render_template, redirect_to, found_object_or_404, is_htmx
)


router = APIRouter(tags=["Playlists"], prefix="/api/playlist")


@router.get("/", response_class=HTMLResponse)
async def get_all_playlist(request: Request):
    qry = Playlist.objects.all()
    context = {
        "playlists": qry
    }
    return render_template(request, "playlists/list.html", context)


@router.get("/create", response_class=HTMLResponse)
@login_required
async def create_playlist(request: Request):
    return render_template(request, "playlists/create.html", {})


@router.post("/create", response_class=HTMLResponse)
@login_required
async def create_playlist(request: Request, title: str = Form(...)):
    raw_data = {
        "user_id": request.user.username,
        "title": title
    }
    data, errors = utils.valid_schema_data(PlaylistCreate, raw_data)
    context = {"data": data, "errors": errors}
    if errors:
        return render_template(request, "playlists/create.html", context, status_code=400)
    obj = Playlist.objects.create(**data)
    redirect_path = obj.path or "api/playlist/create"
    return redirect_to(redirect_path)


@router.get("/{db_id}", response_class=HTMLResponse)
async def get_playlist(request: Request, db_id: uuid.UUID):
    qry = found_object_or_404(Playlist, db_id=db_id)
    context = {
        "playlist": qry,
        "videos": qry.get_videos()
    }
    return render_template(request, f"playlists/details.html", context)


@router.get("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
async def playlist_create_video(request: Request, db_id: uuid.UUID, isHTMX=Depends(is_htmx),):
    context = {"db_id": db_id}
    if not isHTMX:
        raise StarletteHTTPException(status_code=400)
    return render_template(request, "playlists/htmx/add-video.html", context)


@router.post("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
async def playlist_create_video(
        request: Request, db_id: uuid.UUID, isHTMX=Depends(is_htmx),
        url: str = Form(...), title: str = Form(...),
):
    raw_data = {
        "url": url,
        "user_id": request.user.username,
        "title": title,
        "playlist_id": db_id
    }
    data, errors = utils.valid_schema_data(PlaylistVideoCreate, raw_data)
    redirect_path = data.get('path') or f"/api/playlist/{db_id}"
    if not isHTMX:
        raise StarletteHTTPException(status_code=400)
    if errors:
        context = {"data": data, "errors": errors, "url": url, "db_id": db_id}
        return render_template(request, "playlists/htmx/add-video.html", context, status_code=400)
    context = {"path": redirect_path, "title": data.get('title')}
    return render_template(request, "videos/htmx/link.html", context)


@router.post("/{db_id}/{host_id}/delete", response_class=HTMLResponse)
async def remove_video_from_playlist(
        request: Request, db_id: uuid.UUID, host_id: str,
        isHTMX: bool = Depends(is_htmx),
        index: Optional[int] = Form(default=None)
):
    if not isHTMX:
        raise StarletteHTTPException(status_code=400)
    try:
        qry = found_object_or_404(Playlist, db_id=db_id)
    except Exception as e:
        return HTMLResponse(f"Error {e}, Please reload the page")
    if not request.user.is_authenticated:
        return HTMLResponse("You must be logged in to carry out this action")
    if isinstance(index, int):
        host_id = qry.host_ids
        host_id.pop(index)
        qry.add_host_ids(host_ids=host_id, replace_all=True)
    return HTMLResponse("Deleted")
