from typing import List, Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class Technician(BaseModel):
    id: str
    name: str
    skills: List[str] = []
    currentLoad: int = 0


class IntelligentRoutingRequest(BaseAIRequest):
    ticketId: str
    category: str
    priority: str
    availableTechs: List[Technician]


class RoutingRecommendation(BaseModel):
    suggestedAssigneeId: Optional[str] = None
    alternativeAssigneeIds: List[str] = Field(default_factory=list)
    reasoning: str


IntelligentRoutingResponse = AIResponsePayload[RoutingRecommendation]
