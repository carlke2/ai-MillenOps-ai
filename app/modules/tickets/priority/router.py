from fastapi import APIRouter
from app.modules.tickets.priority.schemas import (
    PrioritySuggestionRequest,
    PrioritySuggestionResponse
)
from app.modules.tickets.priority.service import suggest_priority

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Priority"]
)

@router.post("/priority", response_model=PrioritySuggestionResponse)
def suggest_priority_endpoint(payload: PrioritySuggestionRequest):
    return suggest_priority(payload)
