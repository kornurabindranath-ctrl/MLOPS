from app.services.prediction_service import predict_customer


def test_predict_customer(mocker):
    mocker.patch(
        "app.services.prediction_service.get_customer_features",
        return_value={
            "salary": 200000,
            "total_spend": 100000,
            "transaction_count": 20,
        },
    )

    result = predict_customer(1)

    assert result["customer_id"] == 1
    assert result["prediction"] == "Premium"
    assert result["probability"] == 1.0
