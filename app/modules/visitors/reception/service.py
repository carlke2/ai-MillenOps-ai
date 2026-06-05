from app.modules.visitors.reception.schemas import VisitorReceptionRequest
from app.modules.visitors.reception.model import classify_reception_intent_with_model

def classify_reception_intent(payload: VisitorReceptionRequest):
    return classify_reception_intent_with_model(payload)
