from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from api.v1.app import utils
from api.v1.app.models import Video
from api.v1.app.schemas import VideoCreate
from api.v1.app.shortcuts import render_template, redirect_to, found_object_or_404
from api.v1.app.decorators import login_required


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
async def create_video(request: Request):
    return render_template(request, "videos/create.html", {})


@router.post("/create", response_class=HTMLResponse)
@login_required
async def create_video(request: Request, url: str = Form(...), title: str = Form(...)):
    raw_data = {
        "url": url,
        "user_id": request.user.username,
        "title": title
    }
    data, errors = utils.valid_schema_data(VideoCreate, raw_data)
    context = {"data": data, "errors": errors, "url": url}
    if errors:
        return render_template(request, "videos/create.html", context, status_code=400)
    redirect_path = data.get('path') or "/videos/create"
    return redirect_to(redirect_path)


@router.get("/{host_id}", response_class=HTMLResponse)
async def get_video(request: Request, host_id: str):
    qry = found_object_or_404(Video, host_id=host_id)
    context = {
        "host_id": host_id,
        "video": qry
    }
    return render_template(request, f"videos/details.html", context)


