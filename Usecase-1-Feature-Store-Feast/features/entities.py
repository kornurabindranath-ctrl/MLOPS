from feast import Entity
from feast.value_type import ValueType

customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    value_type=ValueType.INT64,
)

transaction = Entity(
    name="transaction",
    join_keys=["transaction_id"],
    value_type=ValueType.INT64,
)
