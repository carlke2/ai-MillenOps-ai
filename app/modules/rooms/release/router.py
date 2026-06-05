from fastapi import APIRouter
from app.modules.rooms.release.schemas import (
    SmartRoomReleaseRequest,
    SmartRoomReleaseResponse
)
from app.modules.rooms.release.service import evaluate_room_release

router = APIRouter(
    prefix="/rooms",
    tags=["Smart Room Release"]
)

@router.post("/release-evaluation", response_model=SmartRoomReleaseResponse)
def evaluate_room_release_endpoint(payload: SmartRoomReleaseRequest):
    return evaluate_room_release(payload)
