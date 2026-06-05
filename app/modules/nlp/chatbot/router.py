from fastapi import APIRouter
from app.modules.nlp.chatbot.schemas import (
    ChatbotRequest,
    UserHelpChatbotResponse
)
from app.modules.nlp.chatbot.service import get_chatbot_response

router = APIRouter(
    prefix="/nlp",
    tags=["User Help Chatbot"]
)

@router.post("/chatbot", response_model=UserHelpChatbotResponse)
def chatbot_endpoint(payload: ChatbotRequest):
    return get_chatbot_response(payload)
