from fastapi import APIRouter
from app.modules.tickets.routing.schemas import (
    IntelligentRoutingRequest,
    IntelligentRoutingResponse
)
from app.modules.tickets.routing.service import route_ticket

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Routing"]
)

@router.post("/route", response_model=IntelligentRoutingResponse)
def route_ticket_endpoint(payload: IntelligentRoutingRequest):
    return route_ticket(payload)
