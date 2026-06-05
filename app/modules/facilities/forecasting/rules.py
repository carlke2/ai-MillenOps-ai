from app.core.config import settings
from app.common.responses import create_ai_response
from app.modules.facilities.forecasting.schemas import FacilityForecastingRequest

def forecast_usage_with_rules(payload: FacilityForecastingRequest):
    data = payload.historicalUsageData
    
    if not data:
        return create_ai_response(
            capability="facility-forecasting",
            correlation_id=payload.correlationId,
            confidence=1.0,
            recommendation={
                "predictedOccupancyRate": 0.0,
                "predictedVisitorCount": 0,
                "peakHours": []
            },
            explanation="No historical data provided for forecasting.",
            model_version=settings.DEFAULT_MODEL_VERSION
        )

    # Simple Average
    avg_occ = sum(d.occupancyRate for d in data) / len(data)
    avg_visitors = sum(d.visitorCount for d in data) / len(data)
    
    # Mocking peak hours
    peak_hours = ["10:00 AM", "02:00 PM"]
    
    return create_ai_response(
        capability="facility-forecasting",
        correlation_id=payload.correlationId,
        confidence=0.60, # Rule-based forecast is low confidence
        recommendation={
            "predictedOccupancyRate": round(avg_occ, 2),
            "predictedVisitorCount": int(avg_visitors),
            "peakHours": peak_hours,
            "confidenceInterval": 0.15
        },
        explanation=f"Forecast based on {len(data)} historical data points (moving average).",
        model_version=settings.DEFAULT_MODEL_VERSION
    )
