from app.modules.workforce.insight.schemas import WorkforceInsightRequest
from app.modules.workforce.insight.rules import analyze_workforce_performance_with_rules

def analyze_performance_with_model(payload: WorkforceInsightRequest):
    return analyze_workforce_performance_with_rules(payload)
