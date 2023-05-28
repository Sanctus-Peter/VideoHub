import uuid
from typing import Optional

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse

from api.v1.app import utils
from api.v1.app.models import Video, WatchEvent
from api.v1.app.schemas import VideoCreate
from api.v1.app.decorators import login_required
from api.v1.app.shortcuts import (
    render_template, redirect_to, found_object_or_404, is_htmx
)

router = APIRouter(tags=["Videos"], prefix="/api/video")


@router.get("/", response_class=HTMLResponse)
async def get_all_video(request: Request):
    qry = Video.objects.all()
    context = {
        "video_list": qry
    }
    return render_template(request, "videos/list.html", context)


@router.get("/details", response_class=HTMLResponse)
async def get_video_details(request: Request):
    return render_template(request, "videos/details.html", {})


@router.get("/create", response_class=HTMLResponse)
@login_required
async def create_video(request: Request, isHTMX=Depends(is_htmx), playlist_id: Optional[uuid.UUID] = None):
    if isHTMX:
        return render_template(request, "videos/htmx/create.html", {})
    return render_template(request, "videos/create.html", {})


@router.post("/create", response_class=HTMLResponse)
@login_required
async def create_video(
        request: Request, isHTMX=Depends(is_htmx),
        url: str = Form(...), title: str = Form(...),
):
    raw_data = {
        "url": url,
        "user_id": request.user.username,
        "title": title
    }
    data, errors = utils.valid_schema_data(VideoCreate, raw_data)
    redirect_path = data.get('path') or "/videos/create"
    if isHTMX:
        context = {
            "path": redirect_path,
            "title": data.get('title'),
            "errors": errors,
        }
        if errors:
            return render_template(request, "videos/htmx/create.html", context)
        return render_template(request, "videos/htmx/link.html", context)
    context = {"data": data, "errors": errors, "url": url}
    if errors:
        return render_template(request, "videos/create.html", context, status_code=400)
    return redirect_to(redirect_path)


@router.get("/{host_id}", response_class=HTMLResponse)
async def get_video(request: Request, host_id: str):
    qry = found_object_or_404(Video, host_id=host_id)
    start_time = 0
    if request.user.is_authenticated:
        user_id = request.user.username
        start_time = WatchEvent.get_resume_time(host_id=host_id, user_id=user_id)
    context = {
        "host_id": host_id,
        "start_time": start_time,
        "video": qry
    }
    return render_template(request, f"videos/details.html", context)
