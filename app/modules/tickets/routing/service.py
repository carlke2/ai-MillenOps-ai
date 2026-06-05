from app.modules.tickets.routing.schemas import IntelligentRoutingRequest
from app.modules.tickets.routing.model import route_ticket_with_model

def route_ticket(payload: IntelligentRoutingRequest):
    return route_ticket_with_model(payload)
