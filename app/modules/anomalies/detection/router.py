from fastapi import APIRouter
from app.modules.anomalies.detection.schemas import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse
)
from app.modules.anomalies.detection.service import detect_anomaly

router = APIRouter(
    prefix="/anomalies",
    tags=["Anomaly Detection"]
)

@router.post("/detect", response_model=AnomalyDetectionResponse)
def detect_anomaly_endpoint(payload: AnomalyDetectionRequest):
    return detect_anomaly(payload)
