from app.modules.tickets.priority.schemas import PrioritySuggestionRequest
from app.modules.tickets.priority.rules import suggest_priority_with_rules

def suggest_priority_with_model(payload: PrioritySuggestionRequest):
    # For now, there is no trained ML model for priority.
    # We fallback to the rule-based approach immediately.
    return suggest_priority_with_rules(payload)
