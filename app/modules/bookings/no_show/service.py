from app.modules.bookings.no_show.schemas import NoShowPredictionRequest
from app.modules.bookings.no_show.model import predict_no_show_with_model

def predict_no_show(payload: NoShowPredictionRequest):
    return predict_no_show_with_model(payload)
