from app.modules.nlp.chatbot.schemas import ChatbotRequest
from app.modules.nlp.chatbot.model import get_chatbot_response_with_model

def get_chatbot_response(payload: ChatbotRequest):
    return get_chatbot_response_with_model(payload)
