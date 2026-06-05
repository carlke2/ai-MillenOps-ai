from fastapi import APIRouter
from app.modules.rooms.recommendation.schemas import (
    RoomRecommendationRequest,
    RoomRecommendationResponse
)
from app.modules.rooms.recommendation.service import recommend_rooms

router = APIRouter(
    prefix="/rooms",
    tags=["Room Recommendation"]
)

@router.post("/recommend", response_model=RoomRecommendationResponse)
def recommend_rooms_endpoint(payload: RoomRecommendationRequest):
    return recommend_rooms(payload)
