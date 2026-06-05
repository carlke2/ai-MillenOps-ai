from app.modules.rooms.recommendation.schemas import RoomRecommendationRequest
from app.modules.rooms.recommendation.rules import recommend_rooms_with_rules

def recommend_rooms_with_model(payload: RoomRecommendationRequest):
    return recommend_rooms_with_rules(payload)
