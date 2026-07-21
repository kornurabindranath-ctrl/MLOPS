from datetime import timedelta

from feast import FeatureView, Field
from feast.types import Float32, Int64, String

from .entities import customer, transaction
from .data_sources import customer_source, transaction_source

# -----------------------------
# Customer Feature View
# -----------------------------

customer_feature_view = FeatureView(
    name="customer_feature_view",
    entities=[customer],
    ttl=timedelta(days=365),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="salary", dtype=Float32),
        Field(name="city", dtype=String),
    ],
    source=customer_source,
)

# -----------------------------
# Transaction Feature View
# -----------------------------

transaction_feature_view = FeatureView(
    name="transaction_feature_view",
    entities=[transaction],
    ttl=timedelta(days=365),
    schema=[
        Field(name="customer_id", dtype=Int64),
        Field(name="amount", dtype=Float32),
        Field(name="merchant", dtype=String),
        Field(name="category", dtype=String),
    ],
    source=transaction_source,
)

from feast.types import Float32, Int64

from .data_sources import customer_aggregate_source

customer_aggregate_feature_view = FeatureView(
    name="customer_aggregate_feature_view",
    entities=[customer],
    ttl=timedelta(days=365),
    schema=[
        Field(name="total_spend", dtype=Float32),
        Field(name="avg_transaction", dtype=Float32),
        Field(name="transaction_count", dtype=Int64),
        Field(name="max_transaction", dtype=Float32),
    ],
    source=customer_aggregate_source,
)
