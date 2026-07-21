from feast import FeatureStore

store = FeatureStore(repo_path=".")


def get_customer_features(customer_id: int) -> dict:
    response = store.get_online_features(
        features=[
            "customer_feature_view:age",
            "customer_feature_view:salary",
            "customer_feature_view:city",
            "customer_aggregate_feature_view:total_spend",
            "customer_aggregate_feature_view:avg_transaction",
            "customer_aggregate_feature_view:transaction_count",
            "customer_aggregate_feature_view:max_transaction",
        ],
        entity_rows=[
            {
                "customer_id": customer_id
            }
        ],
    )

    data = response.to_dict()

    return {
        key: value[0]
        for key, value in data.items()
    }
