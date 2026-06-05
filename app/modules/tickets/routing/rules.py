from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.tickets.routing.schemas import IntelligentRoutingRequest

def route_ticket_with_rules(payload: IntelligentRoutingRequest):
    category = payload.category.lower()
    techs = payload.availableTechs
    
    if not techs:
        return create_ai_response(
            capability="intelligent-routing",
            correlation_id=payload.correlationId,
            confidence=1.0,
            recommendation={
                "suggestedAssigneeId": None,
                "alternativeAssigneeIds": [],
                "reasoning": "No available technicians provided for routing."
            },
            explanation="No technicians available in the pool.",
            model_version=settings.DEFAULT_MODEL_VERSION
        )

    # Scoring technicians
    scored_techs = []
    for tech in techs:
        score = 0
        has_skill = any(skill.lower() in category or category in skill.lower() for skill in tech.skills)
        
        if has_skill:
            score += 100
        
        # Lower load is better (subtract load from score)
        score -= tech.currentLoad * 10
        
        scored_techs.append({
            "id": tech.id,
            "score": score,
            "has_skill": has_skill,
            "load": tech.currentLoad
        })
    
    # Sort by score descending
    scored_techs.sort(key=lambda x: x["score"], reverse=True)
    
    best = scored_techs[0]
    alternatives = [t["id"] for t in scored_techs[1:3]]
    
    reason = f"Selected based on skill match and current load ({best['load']} tickets)."
    if not best["has_skill"]:
        reason = f"No exact skill match found. Selected technician with lowest load ({best['load']} tickets)."

    confidence = 0.85 if best["has_skill"] else 0.50

    return create_ai_response(
        capability="intelligent-routing",
        correlation_id=payload.correlationId,
        confidence=confidence,
        recommendation={
            "suggestedAssigneeId": best["id"],
            "alternativeAssigneeIds": alternatives,
            "reasoning": reason
        },
        explanation=reason,
        model_version=settings.DEFAULT_MODEL_VERSION
    )
