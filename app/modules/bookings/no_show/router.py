from fastapi import APIRouter
from app.modules.bookings.no_show.schemas import (
    NoShowPredictionRequest,
    NoShowPredictionResponse
)
from app.modules.bookings.no_show.service import predict_no_show

router = APIRouter(
    prefix="/bookings",
    tags=["Booking No-Show Prediction"]
)

@router.post("/predict-no-show", response_model=NoShowPredictionResponse)
def predict_no_show_endpoint(payload: NoShowPredictionRequest):
    return predict_no_show(payload)
