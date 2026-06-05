from app.core.config import DEFAULT_MODEL_VERSION
from app.common.text_cleaning import combine_text
from app.common.responses import create_ai_response
from app.modules.tickets.classification.schemas import TicketClassificationRequest


CATEGORY_RULES = {
    "AV / Projector": [
        "projector", "hdmi", "display", "screen", "presentation", "av", "speaker", "microphone"
    ],
    "Network": [
        "wifi", "wi-fi", "internet", "network", "vpn", "router", "connection", "access point"
    ],
    "HVAC / Facility": [
        "ac", "air conditioner", "cooling", "heating", "temperature", "hvac", "light", "lighting", "power"
    ],
    "Access Control": [
        "access", "badge", "door", "lock", "entry", "card", "security gate"
    ],
    "IT": [
        "laptop", "computer", "software", "account", "password", "email", "printer", "system", "login"
    ],
    "Workspace / Meeting Room": [
        "chair", "table", "desk", "furniture", "cleaning", "room dirty", "workspace", "broken chair"
    ],
    "Visitor-related": [
        "visitor", "guest", "reception", "host", "check-in", "checkin", "visitor badge"
    ],
}


def classify_with_rules(payload: TicketClassificationRequest):
    metadata_text = ""

    if payload.metadata:
        safe_values = []
        for value in payload.metadata.values():
            if isinstance(value, (str, int, float, bool)):
                safe_values.append(str(value))
            elif isinstance(value, list):
                safe_values.extend([str(item) for item in value if isinstance(item, (str, int, float, bool))])
        metadata_text = " ".join(safe_values)

    text = combine_text(
        payload.title,
        payload.description,
        payload.roomName,
        payload.department,
        metadata_text
    )

    category_scores = []

    for category, keywords in CATEGORY_RULES.items():
        matched_terms = [word for word in keywords if word in text]
        score = len(matched_terms)

        if score > 0:
            confidence = min(0.95, 0.55 + (score * 0.12))
            category_scores.append({
                "category": category,
                "score": score,
                "confidence": round(confidence, 2),
                "matchedTerms": matched_terms
            })

    if not category_scores:
        return create_ai_response(
            capability="ticket-classification",
            correlation_id=payload.correlationId,
            confidence=0.45,
            recommendation={
                "category": "General Service",
                "alternativeCategories": []
            },
            explanation="No strong category signal found. Manual review recommended.",
            model_version=DEFAULT_MODEL_VERSION
        )

    category_scores.sort(key=lambda item: item["score"], reverse=True)

    best = category_scores[0]
    alternatives = [
        {
            "category": item["category"],
            "confidence": item["confidence"]
        }
        for item in category_scores[1:3]
    ]

    return create_ai_response(
        capability="ticket-classification",
        correlation_id=payload.correlationId,
        confidence=best["confidence"],
        recommendation={
            "category": best["category"],
            "alternativeCategories": alternatives
        },
        explanation=f"Matched keywords: {', '.join(best['matchedTerms'])}",
        model_version=DEFAULT_MODEL_VERSION
    )
