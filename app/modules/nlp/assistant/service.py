from app.modules.nlp.assistant.schemas import MeetingAssistantRequest
from app.modules.nlp.assistant.model import parse_meeting_intent_with_model

def parse_meeting_intent(payload: MeetingAssistantRequest):
    return parse_meeting_intent_with_model(payload)
