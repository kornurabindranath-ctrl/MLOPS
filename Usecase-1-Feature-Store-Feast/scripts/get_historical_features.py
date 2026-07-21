from feast import FeatureStore
import pandas as pd

# Connect to the Feature Store
store = FeatureStore(repo_path=".")

# Load customer data
customers = pd.read_parquet("data/customers.parquet")

# Build the entity dataframe
entity_df = customers[
    ["customer_id", "event_timestamp"]
].copy()

print("=" * 60)
print("Entity DataFrame")
print("=" * 60)
print(entity_df.head())

# Retrieve historical features
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "customer_feature_view:age",
        "customer_feature_view:salary",
        "customer_feature_view:city",
    ],
).to_df()

print("\n" + "=" * 60)
print("Training Dataset")
print("=" * 60)
print(training_df.head())

print("\nShape:", training_df.shape)
