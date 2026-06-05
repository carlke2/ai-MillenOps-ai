from fastapi import APIRouter
from app.modules.workforce.insight.schemas import (
    WorkforceInsightRequest,
    WorkforceInsightResponse
)
from app.modules.workforce.insight.service import analyze_performance

router = APIRouter(
    prefix="/workforce",
    tags=["Workforce Insight"]
)

@router.post("/insight", response_model=WorkforceInsightResponse)
def analyze_performance_endpoint(payload: WorkforceInsightRequest):
    return analyze_performance(payload)
