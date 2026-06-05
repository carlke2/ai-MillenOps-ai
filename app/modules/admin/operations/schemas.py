from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class AdminOperationsRequest(BaseAIRequest):
    operationDate: str
    dailyTickets: int
    dailyBookings: int
    activeAlerts: int


class AdminOperationsRecommendation(BaseModel):
    operationalEfficiencyScore: float = Field(..., ge=0, le=100)
    bottleneckIdentified: bool
    suggestedAction: str
    reasoning: str


AdminOperationsResponse = AIResponsePayload[AdminOperationsRecommendation]
