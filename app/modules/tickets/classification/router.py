from fastapi import APIRouter
from app.modules.tickets.classification.schemas import (
    TicketClassificationRequest,
    TicketClassificationResponse
)
from app.modules.tickets.classification.service import classify_ticket

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Classification"]
)


@router.post("/classify", response_model=TicketClassificationResponse)
def classify_ticket_endpoint(payload: TicketClassificationRequest):
    return classify_ticket(payload)
