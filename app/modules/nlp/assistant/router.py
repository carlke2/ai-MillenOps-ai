from fastapi import APIRouter
from app.modules.nlp.assistant.schemas import (
    MeetingAssistantRequest,
    MeetingAssistantResponse
)
from app.modules.nlp.assistant.service import parse_meeting_intent

router = APIRouter(
    prefix="/nlp",
    tags=["NLP Meeting Assistant"]
)

@router.post("/parse-intent", response_model=MeetingAssistantResponse)
def parse_meeting_intent_endpoint(payload: MeetingAssistantRequest):
    return parse_meeting_intent(payload)
