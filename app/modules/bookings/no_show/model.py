from app.modules.bookings.no_show.schemas import NoShowPredictionRequest
from app.modules.bookings.no_show.rules import predict_no_show_with_rules

def predict_no_show_with_model(payload: NoShowPredictionRequest):
    return predict_no_show_with_rules(payload)
