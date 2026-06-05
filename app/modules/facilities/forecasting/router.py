from fastapi import APIRouter
from app.modules.facilities.forecasting.schemas import (
    FacilityForecastingRequest,
    FacilityForecastingResponse
)
from app.modules.facilities.forecasting.service import forecast_usage

router = APIRouter(
    prefix="/facilities",
    tags=["Facility Usage Forecasting"]
)

@router.post("/forecast", response_model=FacilityForecastingResponse)
def forecast_usage_endpoint(payload: FacilityForecastingRequest):
    return forecast_usage(payload)
