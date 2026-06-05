from app.modules.nlp.chatbot.schemas import ChatbotRequest
from app.modules.nlp.chatbot.rules import get_chatbot_response_with_rules

def get_chatbot_response_with_model(payload: ChatbotRequest):
    return get_chatbot_response_with_rules(payload)
