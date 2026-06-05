from fastapi import APIRouter
from app.modules.meetings.reminders.schemas import (
    MeetingReminderRequest,
    MeetingReminderResponse
)
from app.modules.meetings.reminders.service import schedule_reminder

router = APIRouter(
    prefix="/meetings",
    tags=["Meeting Reminders"]
)

@router.post("/reminders", response_model=MeetingReminderResponse)
def schedule_reminder_endpoint(payload: MeetingReminderRequest):
    return schedule_reminder(payload)
