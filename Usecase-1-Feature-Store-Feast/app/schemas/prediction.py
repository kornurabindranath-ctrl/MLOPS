from pydantic import BaseModel


class PredictionRequest(BaseModel):
    customer_id: int


class PredictionResponse(BaseModel):
    customer_id: int
    prediction: str
    probability: float
    features: dict
