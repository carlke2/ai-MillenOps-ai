from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.anomalies.detection.schemas import AnomalyDetectionRequest

def detect_anomaly_with_rules(payload: AnomalyDetectionRequest):
    avg = payload.historicalAverage
    val = payload.currentValue
    
    if avg == 0:
        deviation = 100.0 if val > 0 else 0.0
    else:
        deviation = abs(val - avg) / avg * 100.0
        
    is_anomaly = False
    severity = "LOW"
    
    # Simple sigma-based logic (mocked)
    # If deviation > 50% from average, we flag it
    if deviation > 100.0:
        is_anomaly = True
        severity = "HIGH"
    elif deviation > 50.0:
        is_anomaly = True
        severity = "MEDIUM"
    elif deviation > 30.0:
        is_anomaly = True
        severity = "LOW"

    reason = f"Current value {val} is {deviation:.1f}% deviated from historical average of {avg}."
    if is_anomaly:
        reason = f"ANOMALY DETECTED: {reason}"
    else:
        reason = f"NORMAL: {reason}"

    return create_ai_response(
        capability="anomaly-detection",
        correlation_id=payload.correlationId,
        confidence=0.90,
        recommendation={
            "isAnomaly": is_anomaly,
            "severity": severity,
            "deviationPercent": round(deviation, 2),
            "reasoning": reason
        },
        explanation=f"Anomaly check for {payload.metricName}: {is_anomaly}.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
