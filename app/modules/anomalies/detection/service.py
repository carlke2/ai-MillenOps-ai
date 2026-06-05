from app.modules.anomalies.detection.schemas import AnomalyDetectionRequest
from app.modules.anomalies.detection.model import detect_anomaly_with_model

def detect_anomaly(payload: AnomalyDetectionRequest):
    return detect_anomaly_with_model(payload)
