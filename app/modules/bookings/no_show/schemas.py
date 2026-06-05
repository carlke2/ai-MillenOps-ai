from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class NoShowPredictionRequest(BaseAIRequest):
    bookingId: str
    hostId: str
    attendeeCount: int
    isRecurring: bool
    timeSinceBooking: int  # e.g., minutes since booking was created


class NoShowRecommendation(BaseModel):
    noShowProbability: float = Field(..., ge=0.0, le=1.0)
    riskLevel: str = Field(..., description="LOW, MEDIUM, or HIGH")
    reasoning: str


NoShowPredictionResponse = AIResponsePayload[NoShowRecommendation]
