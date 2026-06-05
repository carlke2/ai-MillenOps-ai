from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.rooms.release.schemas import SmartRoomReleaseRequest

def evaluate_room_release_with_rules(payload: SmartRoomReleaseRequest):
    should_release = False
    wait_mins = 15
    factors = []
    
    if payload.currentOccupancy is True:
        should_release = False
        wait_mins = 0
        factors.append("Room is currently occupied.")
    elif payload.isNoShowPredicted:
        should_release = True
        wait_mins = 10
        factors.append("No-show is predicted for this booking.")
        
        if payload.currentOccupancy is False:
            wait_mins = 5
            factors.append("Occupancy sensor confirms room is empty.")
    else:
        should_release = False
        wait_mins = 15
        factors.append("Standard no-show grace period.")

    reason = " ".join(factors)
    
    return create_ai_response(
        capability="smart-room-release",
        correlation_id=payload.correlationId,
        confidence=0.85,
        recommendation={
            "shouldRelease": should_release,
            "waitMinutes": wait_mins,
            "reasoning": reason
        },
        explanation=f"Room release decision: {should_release} with {wait_mins} min wait.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
