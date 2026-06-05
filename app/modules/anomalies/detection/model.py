from app.modules.anomalies.detection.schemas import AnomalyDetectionRequest
from app.modules.anomalies.detection.rules import detect_anomaly_with_rules

def detect_anomaly_with_model(payload: AnomalyDetectionRequest):
    return detect_anomaly_with_rules(payload)
