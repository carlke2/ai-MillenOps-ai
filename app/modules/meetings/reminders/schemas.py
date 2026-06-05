from typing import Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class MeetingReminderRequest(BaseAIRequest):
    bookingId: str
    endTime: str
    nextBookingStartTime: Optional[str] = None


class ReminderRecommendation(BaseModel):
    sendReminderAt: str = Field(..., description="ISO datetime string when the reminder should be sent")
    reminderMessage: str
    isUrgent: bool = False


MeetingReminderResponse = AIResponsePayload[ReminderRecommendation]
