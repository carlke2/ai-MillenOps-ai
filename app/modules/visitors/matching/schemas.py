from typing import List, Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class Employee(BaseModel):
    id: str
    name: str
    department: str
    role: str


class VisitorMatchingRequest(BaseAIRequest):
    requestedHostName: str
    visitorPurpose: Optional[str] = None
    employeeDirectory: List[Employee]


class MatchingRecommendation(BaseModel):
    matchedEmployeeId: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list)
    matchScore: float


VisitorMatchingResponse = AIResponsePayload[MatchingRecommendation]
