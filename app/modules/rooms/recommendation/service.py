from app.modules.rooms.recommendation.schemas import RoomRecommendationRequest
from app.modules.rooms.recommendation.model import recommend_rooms_with_model

def recommend_rooms(payload: RoomRecommendationRequest):
    return recommend_rooms_with_model(payload)
