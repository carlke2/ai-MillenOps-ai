from app.modules.rooms.release.schemas import SmartRoomReleaseRequest
from app.modules.rooms.release.model import evaluate_room_release_with_model

def evaluate_room_release(payload: SmartRoomReleaseRequest):
    return evaluate_room_release_with_model(payload)
