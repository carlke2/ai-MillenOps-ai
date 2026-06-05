from datetime import datetime, timedelta
from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.meetings.reminders.schemas import MeetingReminderRequest

def schedule_reminder_with_rules(payload: MeetingReminderRequest):
    end_time = datetime.fromisoformat(payload.endTime.replace("Z", "+00:00"))
    next_start = None
    if payload.nextBookingStartTime:
        next_start = datetime.fromisoformat(payload.nextBookingStartTime.replace("Z", "+00:00"))
        
    is_back_to_back = False
    if next_start and (next_start - end_time) <= timedelta(minutes=15):
        is_back_to_back = True
        
    if is_back_to_back:
        reminder_time = end_time - timedelta(minutes=10)
        message = "Your meeting is ending in 10 minutes. The room is booked immediately after. Please wrap up on time."
        urgent = True
    else:
        reminder_time = end_time - timedelta(minutes=5)
        message = "Your meeting is ending in 5 minutes. Please ensure the room is tidy for the next user."
        urgent = False
        
    # Ensure reminder time is not in the past
    now = datetime.now(reminder_time.tzinfo)
    if reminder_time < now:
        reminder_time = now + timedelta(seconds=10)

    return create_ai_response(
        capability="meeting-reminder",
        correlation_id=payload.correlationId,
        confidence=0.95,
        recommendation={
            "sendReminderAt": reminder_time.isoformat(),
            "reminderMessage": message,
            "isUrgent": urgent
        },
        explanation="Scheduled based on room availability after current meeting.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
