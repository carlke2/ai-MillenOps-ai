from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.visitors.reception.schemas import VisitorReceptionRequest

CATEGORY_KEYWORDS = {
    "DELIVERY": ["delivery", "package", "parcel", "courier", "food", "drop off"],
    "INTERVIEW": ["interview", "job", "hiring", "recruitment", "human resources", "hr"],
    "CLIENT_MEETING": ["client", "customer", "business", "contract", "meeting with"],
    "PERSONAL": ["personal", "friend", "family", "relative", "lunch"],
}

def classify_reception_intent_with_rules(payload: VisitorReceptionRequest):
    text = payload.purposeText.lower()
    
    category = "OTHER"
    urgency = "LOW"
    
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            category = cat
            break
            
    if category == "DELIVERY":
        urgency = "MEDIUM"
    elif category == "INTERVIEW":
        urgency = "HIGH"
        
    reason = f"Classified as {category} based on keywords in purpose text."
    
    return create_ai_response(
        capability="visitor-reception",
        correlation_id=payload.correlationId,
        confidence=0.80,
        recommendation={
            "visitCategory": category,
            "urgency": urgency,
            "reasoning": reason
        },
        explanation=reason,
        model_version=settings.DEFAULT_MODEL_VERSION
    )
