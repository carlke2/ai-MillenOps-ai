from app.modules.nlp.assistant.schemas import MeetingAssistantRequest
from app.modules.nlp.assistant.rules import parse_meeting_intent_with_rules

def parse_meeting_intent_with_model(payload: MeetingAssistantRequest):
    return parse_meeting_intent_with_rules(payload)
