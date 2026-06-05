from app.modules.visitors.matching.schemas import VisitorMatchingRequest
from app.modules.visitors.matching.rules import match_visitor_host_with_rules

def match_visitor_host_with_model(payload: VisitorMatchingRequest):
    return match_visitor_host_with_rules(payload)
