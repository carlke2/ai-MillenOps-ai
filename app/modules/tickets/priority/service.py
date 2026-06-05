from app.modules.tickets.priority.schemas import PrioritySuggestionRequest
from app.modules.tickets.priority.model import suggest_priority_with_model

def suggest_priority(payload: PrioritySuggestionRequest):
    return suggest_priority_with_model(payload)
