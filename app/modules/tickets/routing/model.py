from app.modules.tickets.routing.schemas import IntelligentRoutingRequest
from app.modules.tickets.routing.rules import route_ticket_with_rules

def route_ticket_with_model(payload: IntelligentRoutingRequest):
    # Fallback to rules for baseline implementation
    return route_ticket_with_rules(payload)
