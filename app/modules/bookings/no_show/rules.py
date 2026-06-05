from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.bookings.no_show.schemas import NoShowPredictionRequest

def predict_no_show_with_rules(payload: NoShowPredictionRequest):
    prob = 0.1
    factors = []
    
    if payload.isRecurring:
        prob += 0.2
        factors.append("Recurring meeting (higher risk of abandonment)")
        
    if payload.attendeeCount == 1:
        prob += 0.2
        factors.append("Single attendee (easier to skip)")
    elif payload.attendeeCount > 5:
        prob -= 0.05
        factors.append("Large group (social pressure to attend)")
        
    if payload.timeSinceBooking > 1440: # > 24 hours
        prob += 0.1
        factors.append("Booked long ago (may be forgotten)")

    # Clamp probability
    prob = max(0.0, min(1.0, prob))
    
    if prob < 0.3:
        risk = "LOW"
    elif prob < 0.6:
        risk = "MEDIUM"
    else:
        risk = "HIGH"
        
    reason = " | ".join(factors) if factors else "Standard baseline risk."
    
    return create_ai_response(
        capability="no-show-prediction",
        correlation_id=payload.correlationId,
        confidence=0.70,
        recommendation={
            "noShowProbability": round(prob, 2),
            "riskLevel": risk,
            "reasoning": reason
        },
        explanation=f"Calculated {risk} risk of no-show.",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
