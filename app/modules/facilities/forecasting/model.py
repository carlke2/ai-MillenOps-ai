from app.modules.facilities.forecasting.schemas import FacilityForecastingRequest
from app.modules.facilities.forecasting.rules import forecast_usage_with_rules

def forecast_usage_with_model(payload: FacilityForecastingRequest):
    return forecast_usage_with_rules(payload)
