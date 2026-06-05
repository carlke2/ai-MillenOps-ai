import difflib
from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.visitors.matching.schemas import VisitorMatchingRequest

def match_visitor_host_with_rules(payload: VisitorMatchingRequest):
    requested_name = payload.requestedHostName.lower()
    directory = payload.employeeDirectory
    
    if not directory:
        return create_ai_response(
            capability="visitor-matching",
            correlation_id=payload.correlationId,
            confidence=1.0,
            recommendation={
                "matchedEmployeeId": None,
                "alternatives": [],
                "matchScore": 0.0
            },
            explanation="Employee directory is empty.",
            model_version=settings.DEFAULT_MODEL_VERSION
        )

    scored_matches = []
    
    for emp in directory:
        # Simple fuzzy match score
        score = difflib.SequenceMatcher(None, requested_name, emp.name.lower()).ratio()
        
        scored_matches.append({
            "id": emp.id,
            "name": emp.name,
            "score": score
        })
    
    # Sort by score descending
    scored_matches.sort(key=lambda x: x["score"], reverse=True)
    
    best = scored_matches[0]
    alternatives = [m["id"] for m in scored_matches[1:4] if m["score"] > 0.4]
    
    # If best score is very low, maybe no match
    if best["score"] < 0.5:
        reason = f"No strong match found for '{payload.requestedHostName}'."
        best_id = None
        confidence = 0.40
    else:
        reason = f"Best match for '{payload.requestedHostName}' is {best['name']} with score {best['score']:.2f}."
        best_id = best["id"]
        confidence = best["score"]

    return create_ai_response(
        capability="visitor-matching",
        correlation_id=payload.correlationId,
        confidence=confidence,
        recommendation={
            "matchedEmployeeId": best_id,
            "alternatives": alternatives,
            "matchScore": round(best["score"], 2)
        },
        explanation=reason,
        model_version=settings.DEFAULT_MODEL_VERSION
    )
