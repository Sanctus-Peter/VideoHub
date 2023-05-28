from fastapi import APIRouter, Request

from api.v1.app.models import WatchEvent
from api.v1.app.schemas import WatchEvent as watchEventSchema

router = APIRouter(tags=["Watch Events"], prefix="/api/watch")


@router.post("/events", response_model=watchEventSchema)
async def watch_events(request: Request, watch_event: watchEventSchema):
    data = watch_event.dict()
    if request.user.is_authenticated:
        qry_data = data.copy()
        qry_data.update({"user_id": request.user.username})
        WatchEvent.objects.create(**qry_data)
        return qry_data
    return data
