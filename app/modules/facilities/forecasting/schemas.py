from typing import List, Optional
from pydantic import BaseModel, Field
from app.common.payloads import BaseAIRequest, AIResponsePayload


class UsageDataPoint(BaseModel):
    date: str
    occupancyRate: float
    visitorCount: int


class FacilityForecastingRequest(BaseAIRequest):
    historicalUsageData: List[UsageDataPoint]
    targetDate: str


class ForecastingRecommendation(BaseModel):
    predictedOccupancyRate: float
    predictedVisitorCount: int
    peakHours: List[str] = Field(default_factory=list)
    confidenceInterval: Optional[float] = None


FacilityForecastingResponse = AIResponsePayload[ForecastingRecommendation]
