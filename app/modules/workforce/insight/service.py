from app.modules.workforce.insight.schemas import WorkforceInsightRequest
from app.modules.workforce.insight.model import analyze_performance_with_model

def analyze_performance(payload: WorkforceInsightRequest):
    return analyze_performance_with_model(payload)
