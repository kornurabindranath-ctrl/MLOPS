from fastapi import APIRouter

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.prediction_service import predict_customer

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/predict", response_model=PredictionResponse)
def predict_api(request: PredictionRequest):
    return predict_customer(request.customer_id)
