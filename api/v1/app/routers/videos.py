from fastapi import APIRouter
from api.v1.app.models import Video

router = APIRouter(tags=["Videos"], prefix="/videos")

