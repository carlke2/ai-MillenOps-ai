from app.modules.visitors.reception.schemas import VisitorReceptionRequest
from app.modules.visitors.reception.rules import classify_reception_intent_with_rules

def classify_reception_intent_with_model(payload: VisitorReceptionRequest):
    return classify_reception_intent_with_rules(payload)
