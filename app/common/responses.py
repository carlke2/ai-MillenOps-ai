from typing import Any, TypeVar, Optional
from app.common.payloads import AIResponsePayload

T = TypeVar('T')

def create_ai_response(
    capability: str,
    correlation_id: str,
    recommendation: T,
    confidence: float,
    explanation: str,
    model_version: str,
    success: bool = True
) -> AIResponsePayload[T]:
    return AIResponsePayload[T](
        success=success,
        capability=capability,
        correlationId=correlation_id,
        confidence=round(confidence, 2),
        recommendation=recommendation,
        explanation=explanation,
        modelVersion=model_version
    )
