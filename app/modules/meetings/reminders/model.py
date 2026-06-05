from app.modules.meetings.reminders.schemas import MeetingReminderRequest
from app.modules.meetings.reminders.rules import schedule_reminder_with_rules

def schedule_reminder_with_model(payload: MeetingReminderRequest):
    return schedule_reminder_with_rules(payload)
