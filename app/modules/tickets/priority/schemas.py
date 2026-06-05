from typing import Optional, List
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class PrioritySuggestionRequest(BaseAIRequest):
    ticketId: str
    title: str
    description: Optional[str] = ""
    submitterRole: Optional[str] = None
    category: Optional[str] = None


class PriorityRecommendation(BaseModel):
    priority: str = Field(..., description="LOW, MEDIUM, HIGH, or CRITICAL")
    slaRecommended: str = Field(..., description="Recommended SLA time, e.g., '2h', '24h'")
    contributingFactors: List[str] = Field(default_factory=list, description="Factors that contributed to this priority")

PrioritySuggestionResponse = AIResponsePayload[PriorityRecommendation]
