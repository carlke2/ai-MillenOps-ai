from app.modules.meetings.reminders.schemas import MeetingReminderRequest
from app.modules.meetings.reminders.model import schedule_reminder_with_model

def schedule_reminder(payload: MeetingReminderRequest):
    return schedule_reminder_with_model(payload)
