from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from app.common.payloads import BaseAIRequest, AIResponsePayload


class TicketClassificationRequest(BaseAIRequest):
    ticketId: str
    title: str
    description: Optional[str] = ""
    submitterRole: Optional[str] = None
    roomName: Optional[str] = None
    bookingLinked: bool = False
    department: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AlternativeCategory(BaseModel):
    category: str
    subCategory: Optional[str] = None
    confidence: float


class TicketRecommendation(BaseModel):
    category: str
    subCategory: Optional[str] = None
    alternativeCategories: List[AlternativeCategory] = []

TicketClassificationResponse = AIResponsePayload[TicketRecommendation]
