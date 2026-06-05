from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.admin.operations.schemas import AdminOperationsRequest

def analyze_operations_with_rules(payload: AdminOperationsRequest):
    score = 100.0
    score -= (payload.dailyTickets * 0.5)
    score -= (payload.activeAlerts * 5.0)
    
    score = max(0.0, score)
    
    bottleneck = False
    action = "Continue standard operations."
    
    if score < 40:
        bottleneck = True
        action = "CRITICAL: Immediate reallocation of staff required to handle high ticket volume and alerts."
    elif score < 70:
        bottleneck = True
        action = "ADVISORY: Monitor ticket resolution times closely. Consider opening additional support lanes."
    elif payload.activeAlerts > 5:
        bottleneck = True
        action = "WARNING: Multiple active system alerts. Prioritize infrastructure stability."

    reason = f"Calculated efficiency score of {score:.1f} based on {payload.dailyTickets} tickets and {payload.activeAlerts} alerts."

    return create_ai_response(
        capability="admin-operations-intelligence",
        correlation_id=payload.correlationId,
        confidence=0.80,
        recommendation={
            "operationalEfficiencyScore": round(score, 1),
            "bottleneckIdentified": bottleneck,
            "suggestedAction": action,
            "reasoning": reason
        },
        explanation=f"Operations health check: {score:.1f}% efficiency.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
