from app.models.dummy_model import predict


def test_standard_customer():
    features = {
        "salary": 50000,
        "total_spend": 10000,
        "transaction_count": 2,
    }

    prediction, probability = predict(features)

    assert prediction == "Standard"
    assert probability == 0.0


def test_premium_customer():
    features = {
        "salary": 200000,
        "total_spend": 100000,
        "transaction_count": 20,
    }

    prediction, probability = predict(features)

    assert prediction == "Premium"
    assert probability == 1.0


def test_probability_is_between_0_and_1():
    features = {
        "salary": 150000,
        "total_spend": 30000,
        "transaction_count": 8,
    }

    prediction, probability = predict(features)

    assert prediction in ["Premium", "Standard"]
    assert 0.0 <= probability <= 1.0
