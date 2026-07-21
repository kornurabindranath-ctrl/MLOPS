import pandas as pd

# Load transactions
transactions = pd.read_parquet("data/transactions.parquet")

# Aggregate customer spending
aggregates = (
    transactions.groupby("customer_id")
    .agg(
        total_spend=("amount", "sum"),
        avg_transaction=("amount", "mean"),
        transaction_count=("transaction_id", "count"),
        max_transaction=("amount", "max"),
        last_transaction_time=("timestamp", "max"),
    )
    .reset_index()
)

# Feast requires an event timestamp
aggregates["event_timestamp"] = aggregates["last_transaction_time"]

# Save output
output_path = "data/customer_aggregates.parquet"
aggregates.to_parquet(output_path, index=False)

print("=" * 60)
print("Customer Aggregate Features Created")
print("=" * 60)
print(aggregates.head())
print("\nRows:", len(aggregates))
print(f"\nSaved to: {output_path}")
