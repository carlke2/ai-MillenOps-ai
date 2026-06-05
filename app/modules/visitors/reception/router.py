from fastapi import APIRouter
from app.modules.visitors.reception.schemas import (
    VisitorReceptionRequest,
    VisitorReceptionResponse
)
from app.modules.visitors.reception.service import classify_reception_intent

router = APIRouter(
    prefix="/visitors",
    tags=["Visitor Reception"]
)

@router.post("/reception-intent", response_model=VisitorReceptionResponse)
def classify_reception_intent_endpoint(payload: VisitorReceptionRequest):
    return classify_reception_intent(payload)
