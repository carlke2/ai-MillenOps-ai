from app.modules.rooms.release.schemas import SmartRoomReleaseRequest
from app.modules.rooms.release.rules import evaluate_room_release_with_rules

def evaluate_room_release_with_model(payload: SmartRoomReleaseRequest):
    return evaluate_room_release_with_rules(payload)
