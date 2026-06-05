from app.modules.tickets.classification.schemas import TicketClassificationRequest
from app.modules.tickets.classification.model import classify_with_model


def classify_ticket(payload: TicketClassificationRequest):
    return classify_with_model(payload)
