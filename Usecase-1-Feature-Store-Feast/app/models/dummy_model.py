def predict(features: dict):
    score = 0.0

    salary = features.get("salary") or 0
    total_spend = features.get("total_spend") or 0
    transaction_count = features.get("transaction_count") or 0

    if salary > 150000:
        score += 0.3

    if total_spend > 50000:
        score += 0.4

    if transaction_count > 10:
        score += 0.3

    probability = min(score, 1.0)
    label = "Premium" if probability >= 0.5 else "Standard"

    return label, probability
