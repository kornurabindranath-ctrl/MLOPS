from feast import FeatureService

from .feature_views import (
    customer_feature_view,
    transaction_feature_view,
    customer_aggregate_feature_view,
)

customer_feature_service = FeatureService(
    name="customer_feature_service",
    features=[
        customer_feature_view,
        transaction_feature_view,
        customer_aggregate_feature_view,
    ],
)
