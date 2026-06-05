from typing import Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class VisitorReceptionRequest(BaseAIRequest):
    visitorName: str
    company: Optional[str] = None
    purposeText: str


class ReceptionRecommendation(BaseModel):
    visitCategory: str = Field(..., description="DELIVERY, INTERVIEW, CLIENT_MEETING, PERSONAL, or OTHER")
    urgency: str = Field(..., description="LOW, MEDIUM, or HIGH")
    reasoning: str


VisitorReceptionResponse = AIResponsePayload[ReceptionRecommendation]
