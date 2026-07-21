from feast import FileSource

customer_source = FileSource(
    name="customer_source",
    path="data/customers.parquet",
    timestamp_field="event_timestamp",
)

transaction_source = FileSource(
    name="transaction_source",
    path="data/transactions.parquet",
    timestamp_field="timestamp",
)

customer_aggregate_source = FileSource(
    name="customer_aggregate_source",
    path="data/customer_aggregates.parquet",
    timestamp_field="event_timestamp",
)
