from fastapi import APIRouter
from app.modules.visitors.matching.schemas import (
    VisitorMatchingRequest,
    VisitorMatchingResponse
)
from app.modules.visitors.matching.service import match_visitor_host

router = APIRouter(
    prefix="/visitors",
    tags=["Visitor Matching"]
)

@router.post("/match-host", response_model=VisitorMatchingResponse)
def match_visitor_host_endpoint(payload: VisitorMatchingRequest):
    return match_visitor_host(payload)
