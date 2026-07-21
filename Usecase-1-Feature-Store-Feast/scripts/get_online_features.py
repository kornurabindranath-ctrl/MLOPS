from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = store.get_online_features(
    features=[
        "customer_feature_view:age",
        "customer_feature_view:salary",
        "customer_feature_view:city",
    ],
    entity_rows=[
        {"customer_id": 1},
        {"customer_id": 2},
        {"customer_id": 3},
    ],
).to_dict()

print(features)
