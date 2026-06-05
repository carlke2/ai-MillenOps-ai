from pydantic import BaseModel, Field
from typing import Any, Generic, TypeVar

T = TypeVar('T')

class BaseAIRequest(BaseModel):
    correlationId: str = Field(..., description="Unique identifier from NestJS request for tracing")

class AIResponsePayload(BaseModel, Generic[T]):
    success: bool = Field(True, description="Indicates if the AI execution was successful")
    capability: str = Field(..., description="The name of the AI module (e.g., ticket-classification)")
    correlationId: str = Field(..., description="Unique identifier from NestJS request for tracing")
    recommendation: T = Field(..., description="The module-specific recommendation or prediction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the prediction (0.0 to 1.0)")
    explanation: str = Field(..., description="Human-readable explanation of why this recommendation was made")
    modelVersion: str = Field(..., description="The version of the rule engine or ML model used")
