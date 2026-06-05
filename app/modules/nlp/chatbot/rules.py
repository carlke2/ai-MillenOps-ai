from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.nlp.chatbot.schemas import ChatbotRequest

FAQ_MAP = {
    "wifi": {
        "text": "The guest Wi-Fi network is 'MillenOps-Guest'. No password is required, but you must accept the terms on the portal.",
        "links": ["/help/connectivity"],
        "redirect": None
    },
    "booking": {
        "text": "You can book a room via the 'Bookings' tab on your dashboard. Select a room and a time slot to proceed.",
        "links": ["/help/bookings"],
        "redirect": "/dashboard/bookings/new"
    },
    "ticket": {
        "text": "To report an issue, please create a support ticket. You can find this under the 'Support' section.",
        "links": ["/help/tickets"],
        "redirect": "/dashboard/support/new"
    },
    "visitor": {
        "text": "You can register visitors in advance to speed up their check-in process. Use the 'Visitors' tab.",
        "links": ["/help/visitors"],
        "redirect": "/dashboard/visitors/register"
    }
}

def get_chatbot_response_with_rules(payload: ChatbotRequest):
    text = payload.queryText.lower()
    
    response_data = {
        "text": "I'm not sure about that. Would you like to speak with a human support agent?",
        "links": ["/help/contact"],
        "redirect": None
    }
    
    for key, data in FAQ_MAP.items():
        if key in text:
            response_data = data
            break
            
    return create_ai_response(
        capability="user-help-chatbot",
        correlation_id=payload.correlationId,
        confidence=0.85 if response_data["redirect"] or key in text else 0.40,
        recommendation={
            "responseText": response_data["text"],
            "usefulLinks": response_data["links"],
            "actionRedirect": response_data["redirect"]
        },
        explanation="Matched user query against internal FAQ database.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
