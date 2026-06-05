from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class AnomalyDetectionRequest(BaseAIRequest):
    metricName: str
    currentValue: float
    historicalAverage: float
    thresholdSigma: float = 2.0


class AnomalyRecommendation(BaseModel):
    isAnomaly: bool
    severity: str = Field(..., description="LOW, MEDIUM, or HIGH")
    deviationPercent: float
    reasoning: str


AnomalyDetectionResponse = AIResponsePayload[AnomalyRecommendation]
