from app.core.config import settings
from app.common.text_cleaning import combine_text
from app.common.responses import create_ai_response
from app.modules.tickets.priority.schemas import PrioritySuggestionRequest

CRITICAL_KEYWORDS = ["fire", "flood", "smoke", "injury", "safety", "emergency", "power out", "stuck"]
HIGH_KEYWORDS = ["urgent", "vip", "broken", "offline", "down", "spill", "hazard"]
MEDIUM_KEYWORDS = ["noisy", "warm", "cold", "uncomfortable", "flickering", "slow"]

VIP_ROLES = ["ceo", "cto", "cfo", "vp", "director", "executive"]

def suggest_priority_with_rules(payload: PrioritySuggestionRequest):
    text = combine_text(payload.title, payload.description)
    submitter_role = (payload.submitterRole or "").lower().strip()
    
    factors = []
    priority = "LOW"
    sla = "48h"
    confidence = 0.50
    
    # Check for Critical
    critical_matches = [kw for kw in CRITICAL_KEYWORDS if kw in text]
    if critical_matches:
        priority = "CRITICAL"
        sla = "1h"
        confidence = 0.95
        factors.append(f"Emergency keywords detected: {', '.join(critical_matches)}")
    else:
        # Check for High
        high_matches = [kw for kw in HIGH_KEYWORDS if kw in text]
        if high_matches:
            priority = "HIGH"
            sla = "4h"
            confidence = 0.85
            factors.append(f"High-urgency keywords detected: {', '.join(high_matches)}")
        
        # Check VIP Status
        if submitter_role in VIP_ROLES:
            if priority != "HIGH" and priority != "CRITICAL":
                priority = "HIGH"
                sla = "4h"
                confidence = 0.90
            factors.append(f"VIP submitter role detected: {submitter_role}")
            
        if priority == "LOW":
            # Check Medium
            medium_matches = [kw for kw in MEDIUM_KEYWORDS if kw in text]
            if medium_matches:
                priority = "MEDIUM"
                sla = "24h"
                confidence = 0.75
                factors.append(f"Medium-urgency keywords detected: {', '.join(medium_matches)}")
    
    if priority == "LOW":
        factors.append("No high-priority keywords or VIP signals detected")
        confidence = 0.80

    explanation = "Priority suggested based on keyword heuristics."
    if factors:
        explanation = " | ".join(factors)

    return create_ai_response(
        capability="ticket-priority",
        correlation_id=payload.correlationId,
        confidence=confidence,
        recommendation={
            "priority": priority,
            "slaRecommended": sla,
            "contributingFactors": factors
        },
        explanation=explanation,
        model_version=settings.DEFAULT_MODEL_VERSION
    )
