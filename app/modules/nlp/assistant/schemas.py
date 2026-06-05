from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class ParsedMeetingIntent(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[int] = None
    durationMins: Optional[int] = 60
    subject: Optional[str] = None


class MeetingAssistantRequest(BaseAIRequest):
    intentText: str
    userProfile: Optional[Dict[str, Any]] = None


class MeetingAssistantRecommendation(BaseModel):
    parsedIntent: ParsedMeetingIntent
    actionNeeded: str = Field(..., description="e.g., 'needs_room', 'confirm_booking', 'more_info'")
    replyText: str


MeetingAssistantResponse = AIResponsePayload[MeetingAssistantRecommendation]
