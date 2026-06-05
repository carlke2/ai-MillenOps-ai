from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.rooms.recommendation.schemas import RoomRecommendationRequest

def recommend_rooms_with_rules(payload: RoomRecommendationRequest):
    attendees = payload.attendeeCount
    required_equip = [e.lower() for e in payload.requiredEquipment]
    rooms = payload.availableRooms
    
    if not rooms:
        return create_ai_response(
            capability="room-recommendation",
            correlation_id=payload.correlationId,
            confidence=1.0,
            recommendation={
                "recommendedRoomIds": [],
                "matchScores": {},
                "reasoning": "No available rooms provided."
            },
            explanation="No rooms available in the provided list.",
            model_version=settings.DEFAULT_MODEL_VERSION
        )

    scored_rooms = []
    
    for room in rooms:
        # Hard filters
        if room.capacity < attendees:
            continue
        
        room_equip = [e.lower() for e in room.equipment]
        missing_equip = [e for e in required_equip if e not in room_equip]
        if missing_equip:
            continue
            
        # Scoring
        score = 1.0
        
        # Penalty for oversized rooms (to save large rooms for large groups)
        capacity_ratio = attendees / room.capacity # 1.0 is perfect, 0.1 is very oversized
        score *= (0.5 + 0.5 * capacity_ratio)
        
        # Bonus for floor match
        if payload.preferredFloor is not None and room.floor == payload.preferredFloor:
            score += 0.2
            
        # Small bonus for each extra equipment
        score += len(room_equip) * 0.01
        
        # Cap score at 1.0
        score = min(1.0, score)
        
        scored_rooms.append({
            "id": room.id,
            "name": room.name,
            "score": round(score, 2)
        })
    
    # Sort by score descending
    scored_rooms.sort(key=lambda x: x["score"], reverse=True)
    
    recommended_ids = [r["id"] for r in scored_rooms[:3]]
    match_scores = {r["id"]: r["score"] for r in scored_rooms}
    
    if not recommended_ids:
        reason = "No rooms found that meet the capacity and equipment requirements."
        confidence = 1.0
    else:
        best_name = scored_rooms[0]["name"]
        reason = f"Recommended {best_name} as the best match for {attendees} attendees."
        confidence = 0.90

    return create_ai_response(
        capability="room-recommendation",
        correlation_id=payload.correlationId,
        confidence=confidence,
        recommendation={
            "recommendedRoomIds": recommended_ids,
            "matchScores": match_scores,
            "reasoning": reason
        },
        explanation=reason,
        model_version=settings.DEFAULT_MODEL_VERSION
    )
