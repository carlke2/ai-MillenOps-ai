import re
from datetime import datetime, timedelta
from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.nlp.assistant.schemas import MeetingAssistantRequest, ParsedMeetingIntent

def parse_meeting_intent_with_rules(payload: MeetingAssistantRequest):
    text = payload.intentText.lower()
    
    intent = ParsedMeetingIntent()
    
    # Simple attendee extraction
    attendee_match = re.search(r"(\d+)\s*(?:people|persons|attendees|participants)", text)
    if attendee_match:
        intent.attendees = int(attendee_match.group(1))
    
    # Simple date extraction (relative)
    if "today" in text:
        intent.date = datetime.now().strftime("%Y-%m-%d")
    elif "tomorrow" in text:
        intent.date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "next tuesday" in text:
        # Placeholder logic for next tuesday
        intent.date = "2026-06-09" # Mocking for demo
        
    # Simple time extraction
    time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)", text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3)
        if ampm == "pm" and hour < 12:
            hour += 12
        intent.time = f"{hour:02d}:{minute:02d}"

    # Determine action
    if not intent.date or not intent.time or not intent.attendees:
        action = "more_info"
        reply = "I've started planning your meeting, but I need a bit more detail. Could you tell me the date, time, or number of attendees?"
    else:
        action = "needs_room"
        reply = f"Great! I've parsed your request for a meeting on {intent.date} at {intent.time} for {intent.attendees} people. I'll search for available rooms now."

    return create_ai_response(
        capability="meeting-assistant",
        correlation_id=payload.correlationId,
        confidence=0.75,
        recommendation={
            "parsedIntent": intent,
            "actionNeeded": action,
            "replyText": reply
        },
        explanation="Parsed intent using regex heuristics.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
