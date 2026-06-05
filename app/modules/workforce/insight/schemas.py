from typing import Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class WorkforceInsightRequest(BaseAIRequest):
    technicianId: str
    tasksCompleted: int
    avgResolutionTimeMins: int
    feedbackScore: float = Field(..., ge=0, le=5)


class WorkforceRecommendation(BaseModel):
    productivityScore: float = Field(..., ge=0, le=100)
    performanceInsight: str
    suggestedTraining: Optional[str] = None


WorkforceInsightResponse = AIResponsePayload[WorkforceRecommendation]
