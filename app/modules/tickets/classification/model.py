from app.core.config import settings
from app.common.model_loader import load_joblib_model
from app.common.responses import create_ai_response
from app.modules.tickets.classification.schemas import TicketClassificationRequest
from app.modules.tickets.classification.rules import classify_with_rules

TRAINED_MODEL_VERSION = "ticket-classifier-v1"

_model = None


def get_model():
    global _model

    if _model is None:
        _model = load_joblib_model(settings.TICKET_CLASSIFIER_MODEL_PATH)

    return _model


def build_model_text(payload: TicketClassificationRequest):
    return f"""
    title: {payload.title}
    description: {payload.description or ""}
    room: {payload.roomName or ""}
    department: {payload.department or ""}
    bookingLinked: {payload.bookingLinked}
    """


def classify_with_model(payload: TicketClassificationRequest):
    model = get_model()

    if model is None:
        return classify_with_rules(payload)

    try:
        text = build_model_text(payload)
        predicted_category = model.predict([text])[0]

        confidence = 0.70

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba([text])[0]
            confidence = float(max(probabilities))

        return create_ai_response(
            capability="ticket-classification",
            correlation_id=payload.correlationId,
            confidence=confidence,
            recommendation={
                "category": predicted_category,
                "alternativeCategories": []
            },
            explanation="Category predicted using trained ticket classification model.",
            model_version=TRAINED_MODEL_VERSION
        )

    except Exception:
        return classify_with_rules(payload)
