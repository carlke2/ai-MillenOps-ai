from typing import Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class SmartRoomReleaseRequest(BaseAIRequest):
    bookingId: str
    isNoShowPredicted: bool
    currentOccupancy: Optional[bool] = None


class ReleaseRecommendation(BaseModel):
    shouldRelease: bool
    waitMinutes: int
    reasoning: str


SmartRoomReleaseResponse = AIResponsePayload[ReleaseRecommendation]
