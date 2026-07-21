import logging

from app.models.dummy_model import predict
from app.services.feast_service import get_customer_features

logger = logging.getLogger(__name__)


def predict_customer(customer_id: int):
    logger.info(
        "Fetching customer features",
        extra={"customer_id": customer_id},
    )

    features = get_customer_features(customer_id)

    label, probability = predict(features)

    logger.info(
        "Prediction generated",
        extra={
            "customer_id": customer_id,
            "prediction": label,
        },
    )

    return {
        "customer_id": customer_id,
        "prediction": label,
        "probability": probability,
        "features": features,
    }
