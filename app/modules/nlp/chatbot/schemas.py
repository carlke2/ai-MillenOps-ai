from typing import List, Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class ChatbotRequest(BaseAIRequest):
    queryText: str
    userId: str
    currentContext: Optional[str] = None


class ChatbotRecommendation(BaseModel):
    responseText: str
    usefulLinks: List[str] = Field(default_factory=list)
    actionRedirect: Optional[str] = None


UserHelpChatbotResponse = AIResponsePayload[ChatbotRecommendation]
