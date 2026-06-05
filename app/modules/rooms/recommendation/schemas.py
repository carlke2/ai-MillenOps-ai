from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class Room(BaseModel):
    id: str
    name: str
    capacity: int
    equipment: List[str] = []
    floor: int


class RoomRecommendationRequest(BaseAIRequest):
    attendeeCount: int
    durationMins: int
    requiredEquipment: List[str] = []
    preferredFloor: Optional[int] = None
    availableRooms: List[Room]


class RoomRecommendation(BaseModel):
    recommendedRoomIds: List[str] = Field(default_factory=list)
    matchScores: Dict[str, float] = Field(default_factory=dict, description="Score from 0.0 to 1.0 for each room")
    reasoning: str


RoomRecommendationResponse = AIResponsePayload[RoomRecommendation]
