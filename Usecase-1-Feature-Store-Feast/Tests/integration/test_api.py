from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_predict_api(mocker):
    mocker.patch(
        "app.api.routes.predict_customer",
        return_value={
            "customer_id": 1,
            "prediction": "Premium",
            "probability": 1.0,
            "features": {
                "salary": 200000,
                "total_spend": 100000,
            },
        },
    )

    response = client.post(
        "/predict",
        json={"customer_id": 1},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["customer_id"] == 1
    assert body["prediction"] == "Premium"
    assert body["probability"] == 1.0
