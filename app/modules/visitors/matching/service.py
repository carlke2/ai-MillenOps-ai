from app.modules.visitors.matching.schemas import VisitorMatchingRequest
from app.modules.visitors.matching.model import match_visitor_host_with_model

def match_visitor_host(payload: VisitorMatchingRequest):
    return match_visitor_host_with_model(payload)
