from app.modules.facilities.forecasting.schemas import FacilityForecastingRequest
from app.modules.facilities.forecasting.model import forecast_usage_with_model

def forecast_usage(payload: FacilityForecastingRequest):
    return forecast_usage_with_model(payload)
