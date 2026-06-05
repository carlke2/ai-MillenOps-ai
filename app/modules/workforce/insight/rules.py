from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.workforce.insight.schemas import WorkforceInsightRequest

def analyze_workforce_performance_with_rules(payload: WorkforceInsightRequest):
    # Base productivity score
    # 50 base + (tasks * 2) - (avg_time / 10)
    score = 50.0 + (payload.tasksCompleted * 2.0) - (payload.avgResolutionTimeMins / 5.0)
    
    # Adjust for feedback
    score += (payload.feedbackScore - 3.0) * 10.0
    
    score = max(0.0, min(100.0, score))
    
    insight = "Standard performance level."
    training = None
    
    if score > 85:
        insight = "Excellent performance! High task completion and positive feedback."
    elif score < 40:
        insight = "Performance requires attention. Low productivity or negative feedback detected."
        training = "Efficiency and Customer Service Training"
        
    if payload.feedbackScore < 2.5:
        training = "Customer Communication Workshop"

    return create_ai_response(
        capability="workforce-insight",
        correlation_id=payload.correlationId,
        confidence=0.75,
        recommendation={
            "productivityScore": round(score, 1),
            "performanceInsight": insight,
            "suggestedTraining": training
        },
        explanation=f"Performance analyzed based on {payload.tasksCompleted} tasks and {payload.feedbackScore} feedback score.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
