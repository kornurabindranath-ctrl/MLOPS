# Feature-Store-Feast

check python 

bash
```
python3 --version

pip3 --version
```

create a virtual environment

bash
```
python3 -m venv .venv

source .venv/bin/activate
```

<img width="2884" height="232" alt="image" src="https://github.com/user-attachments/assets/2832672c-4864-49b8-9f07-4ecf2b875fcb" />

# Installing Feast

bash
```

pip install --upgrade pip 

pip install feast

feast version
```

<img width="2870" height="178" alt="image" src="https://github.com/user-attachments/assets/f54ca335-f069-4be6-921d-ed8a3c95364e" />

# Initialize a Feature Repository

bash
```
feast init feature_repo
```

This creates a starter repository.

<img width="2940" height="608" alt="image" src="https://github.com/user-attachments/assets/57dbbb79-bc35-4fb2-bad0-dab25a7cef0a" />


The feature repository is where you define what features exist, where they come from, and how they should be served.

# Directory structure

<img width="2762" height="1064" alt="image" src="https://github.com/user-attachments/assets/85c8ced7-818b-4d51-abc1-939f040a50da" />


# Generate Synthetic Data


Install these packages

bash
```
pip install pandas faker numpy

```

scripts/generate_data.py

bash
```
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_CUSTOMERS = 10000
NUM_TRANSACTIONS = 100000

cities = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata"
]

merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Uber",
    "Apple",
    "Reliance",
    "DMart"
]

categories = [
    "Shopping",
    "Food",
    "Travel",
    "Electronics",
    "Groceries"
]

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "age": random.randint(18,70),
        "city": random.choice(cities),
        "salary": random.randint(30000,250000),
        "account_created": fake.date_between("-10y","today")
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    "../data/customers.csv",
    index=False
)

transactions = []

for transaction_id in range(1, NUM_TRANSACTIONS + 1):

    customer = random.randint(1, NUM_CUSTOMERS)

    timestamp = fake.date_time_between(
        start_date="-365d",
        end_date="now"
    )

    transactions.append({
        "transaction_id": transaction_id,
        "customer_id": customer,
        "amount": round(random.uniform(50,15000),2),
        "merchant": random.choice(merchants),
        "category": random.choice(categories),
        "timestamp": timestamp
    })

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    "../data/transactions.csv",
    index=False
)

print("Customers:", len(customers_df))
print("Transactions:", len(transactions_df))
print("Done!")
```
bash
```
python scripts/generate_data.py
```

<img width="2930" height="974" alt="image" src="https://github.com/user-attachments/assets/6dcbe7e4-f7d0-4064-84ab-54c0c65d10bb" />

now we have data 

<img width="2928" height="1284" alt="image" src="https://github.com/user-attachments/assets/bec6a0a0-0105-42c0-b8be-45bdd3b5cf92" />

# Creating Features

bash
```

```
 adding this in  feature_definitions.py

 bash
```
from customer_features import (
    customer,
    customer_features,
)
```
 This exposes your definitions to Feast.

 run

 bash
 ```
feast apply
 ```

<img width="2934" height="1528" alt="image" src="https://github.com/user-attachments/assets/124b88a8-4837-420f-a8c0-d1a3d7e1f89c" />

got the issue based on the feast is not able to read the csv files then we need to create paraquet files


edit and generate 

bash
```
print("Writing Parquet files...")

customers_df.to_parquet(
    DATA_DIR / "customers.parquet",
    index=False,
)

transactions_df.to_parquet(
    DATA_DIR / "transactions.parquet",
    index=False,
)

print("Parquet files created.")

```
<img width="2802" height="328" alt="image" src="https://github.com/user-attachments/assets/d932e7ef-f568-4b9b-b37f-57ffd4353b7f" />


bash
```
feast apply
```

<img width="2940" height="1648" alt="image" src="https://github.com/user-attachments/assets/11232782-6a2d-43a6-b44b-91aebfcdf230" />
it created a registry containing metadata about your feature store.

# scripts/get_historical_features.py

bash
```
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
```
<img width="2940" height="1372" alt="image" src="https://github.com/user-attachments/assets/df1a9198-959c-42d4-9874-2ee29e5029a9" />


# Online Feature Serving(Redis)

A customer submits a loan application, and your model has only a few milliseconds to respond. Reading Parquet files and performing joins for every request is far too slow.

Suppose a request arrives:

Customer ID = 1025

The model needs:

age
salary
city

immediately.

Without an online store:

Request
   │
   ▼
Read Parquet
   │
Join Data
   │
Return Features

This can take hundreds of milliseconds or more, depending on the data size.

With an online store:

Request
   │
   ▼
Redis
   │
Return Features

Typically this is only a few milliseconds.

starting redis

bash
```
docker run -d \
  --name feast-redis \
  -p 6379:6379 \
  redis:7
```

verify 

<img width="2928" height="286" alt="image" src="https://github.com/user-attachments/assets/a3f51015-9fef-4e67-a79b-be06bb825510" />

# Update feature_store.yaml

bash
```
online_store:
    type: redis
    connection_string: localhost:6379
 ```

 bash
 ```
pip install 'feast[redis]'
```

then apply the feast then validate the green

# Materialize Features

Now we'll copy the latest feature values into Redis.

bash
```
feast materialize-incremental $(date +%Y-%m-%dT%H:%M:%S)

```

<img width="2940" height="340" alt="image" src="https://github.com/user-attachments/assets/c6c36fdb-060e-4aeb-81db-8869cd9788a5" />

# Verify Online Retrieval

bash
```
get_online_features.py


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
```

<img width="2940" height="328" alt="image" src="https://github.com/user-attachments/assets/2ec90fc0-6c23-4205-9c50-f0227baf1d0c" />

| Historical Features          | Online Features                   |
| ---------------------------- | --------------------------------- |
| Used for training            | Used for inference                |
| Reads offline data           | Reads Redis                       |
| Point-in-time correct        | Latest values only                |
| Can process millions of rows | Optimized for low-latency lookups |

# Add a Transaction Entity

bash
```
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
```
# data sources

features/data_sources.py
bash
```


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
```

# Create a Transaction Feature View

bash
```
from datetime import timedelta

from feast import FeatureView, Field
from feast.types import Float32, Int64, String

from .entities import customer, transaction
from .data_sources import customer_source, transaction_source

# -----------------------------
# Customer Feature View
# -----------------------------

customer_feature_view = FeatureView(
    name="customer_feature_view",
    entities=[customer],
    ttl=timedelta(days=365),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="salary", dtype=Float32),
        Field(name="city", dtype=String),
    ],
    source=customer_source,
)

# -----------------------------
# Transaction Feature View
# -----------------------------

transaction_feature_view = FeatureView(
    name="transaction_feature_view",
    entities=[transaction],
    ttl=timedelta(days=365),
    schema=[
        Field(name="customer_id", dtype=Int64),
        Field(name="amount", dtype=Float32),
        Field(name="merchant", dtype=String),
        Field(name="category", dtype=String),
    ],
    source=transaction_source,
)
```

# Update the Feature Service

bash
```
from feast import FeatureService

from .feature_views import (
    customer_feature_view,
    transaction_feature_view,
)

customer_feature_service = FeatureService(
    name="customer_feature_service",
    features=[
        customer_feature_view,
        transaction_feature_view,
    ],
)


```
# feature defintion

bash
```
from features.entities import customer, transaction

from features.data_sources import (
    customer_source,
    transaction_source,
)

from features.feature_views import (
    customer_feature_view,
    transaction_feature_view,
)

from features.feature_services import (
    customer_feature_service,
)
```

bash
```
feast apply 
```
<img width="2940" height="1672" alt="image" src="https://github.com/user-attachments/assets/56f4936a-49c3-48f2-bb60-5d1559939f49" />

# Build a Feature Engineering Pipeline

## Create the aggregation pipeline

scripts/build_customer_aggregates.py

bash
```
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
```
This script represents a batch feature engineering pipeline.

In production, this wouldn't usually be a standalone Python script. It would likely be:

A Spark job
A dbt model
An Airflow DAG
A scheduled ETL pipeline

Its responsibility is to compute features.

Feast's responsibility is to register and serve them.

Keeping those responsibilities separate is a core architectural principle.

<img width="2940" height="830" alt="image" src="https://github.com/user-attachments/assets/39d46b8b-858a-477f-84d0-efe07ee0118c" />

Once aggregation is done add to data sources

bash
```
from feast import FileSource


customer_aggregate_source = FileSource(
    name="customer_aggregate_source",
    path="data/customer_aggregates.parquet",
    timestamp_field="event_timestamp",
)
```
# creating a feature view for aggregated customer data

bash
```
from feast.types import Float32, Int64

from .data_sources import customer_aggregate_source

customer_aggregate_feature_view = FeatureView(
    name="customer_aggregate_feature_view",
    entities=[customer],
    ttl=timedelta(days=365),
    schema=[
        Field(name="total_spend", dtype=Float32),
        Field(name="avg_transaction", dtype=Float32),
        Field(name="transaction_count", dtype=Int64),
        Field(name="max_transaction", dtype=Float32),
    ],
    source=customer_aggregate_source,
)
```

modify feature services with aggregated data

bash
```
from feast import FeatureService

from .feature_views import (
    customer_feature_view,
    transaction_feature_view,
    customer_aggregate_feature_view,
)

customer_feature_service = FeatureService(
    name="customer_feature_service",
    features=[
        customer_feature_view,
        transaction_feature_view,
        customer_aggregate_feature_view,
    ],
)
```

<img width="2932" height="1764" alt="image" src="https://github.com/user-attachments/assets/10e4c5ce-b2a9-4dfb-b312-8824bf52502a" />

Every time you run feast apply, your console shows:

Generating customers...
Generating transactions...
Customer Aggregate Features Created...

That should not happen.

feast apply should only register metadata.

It should NOT:

Generate synthetic data
Build aggregate datasets
Run historical retrieval scripts
Query online features

That means something in your repository is importing and executing Python scripts during feast apply.

These scripts should only run when you execute them directly, for example:

python scripts/generate_data.py
python scripts/build_customer_aggregates.py
python scripts/get_historical_features.py
python scripts/get_online_features.py

They should not execute during:

feast apply

# Build an Inference Service

```
                    Client
                      │
          POST /predict
                      │
                      ▼
              FastAPI Service
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Feast Online Store           ML Model
        │                           │
        └─────────────┬─────────────┘
                      ▼
                Prediction
```

Notice that:

Feast is responsible for serving features
The model is responsible for making predictions
FastAPI orchestrates the two

Keeping these responsibilities separate is a key production design principle.

The service will:

Receive a customer ID.
Fetch online features from Feast.
Build a feature vector.
Run a model (initially a dummy model).
Return a prediction.

This is how many production inference services are structured.

Create the application directory and install fast api and uvicorn

bash
```
mkdir app
pip install fastapi uvicorn
```

## Define the API contract

app/schemas.py:

bash
```
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    customer_id: int


class PredictionResponse(BaseModel):
    customer_id: int
    prediction: str
    probability: float
    features: dict
```

## reusable feast client

bash
```
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
        entity_rows=[{"customer_id": customer_id}],
    )

    data = response.to_dict()

    return {
        key: value[0]
        for key, value in data.items()
    }
```

## dummy model for prediction

bash
```
def predict(features: dict):
    score = 0

    if features["salary"] > 150000:
        score += 0.3

    if features["total_spend"] > 50000:
        score += 0.4

    if features["transaction_count"] > 10:
        score += 0.3

    probability = min(score, 1.0)

    label = "Premium" if probability >= 0.5 else "Standard"

    return label, probability
```
This is intentionally simple. Later we'll replace it with a trained model (for example, a scikit-learn model loaded from disk), but the API won't need to change.

## Build the FastAPI application

bash
```
from fastapi import FastAPI

from app.schemas import PredictionRequest, PredictionResponse
from app.feast_client import get_customer_features
from app.model import predict

app = FastAPI(
    title="Customer Prediction API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict_customer(request: PredictionRequest):
    features = get_customer_features(request.customer_id)

    label, probability = predict(features)

    return PredictionResponse(
        customer_id=request.customer_id,
        prediction=label,
        probability=probability,
        features=features,
    )
```

## start the api

bash
```
uvicorn app.main:app --reload
```
<img width="2932" height="760" alt="image" src="https://github.com/user-attachments/assets/5b8a6c2b-eb9c-42ae-bd8a-84eadf185bdf" />

<img width="2932" height="600" alt="image" src="https://github.com/user-attachments/assets/a9014170-2c9e-428f-aff5-90fa7eff5749" />


forgot to materialize the feature view

<img width="2938" height="372" alt="image" src="https://github.com/user-attachments/assets/5adf79ee-22d7-42da-b05a-2b50d57de893" />

feast apply only updates metadata. It does not load data into Redis.

Testing an API

<img width="2940" height="284" alt="image" src="https://github.com/user-attachments/assets/8998ff15-2e45-47ac-8e2e-9b61b0729645" />


# Dockerize the Inference Service

Before Kubernetes, every production service should be packaged into a reproducible container.


Creating a directory

bash
```
mkdir docker
touch docker/Dockerfile
touch .dockerignore
```

freeze environment

bash
```
pip freeze > requirements.txt
```
<img width="2668" height="1748" alt="image" src="https://github.com/user-attachments/assets/e658f3bd-ef3b-4acd-aa11-6df563b301d2" />

docker ignore

bash
```
.venv
.git
__pycache__
.pytest_cache
*.pyc
*.pyo
*.DS_Store

data/*.csv

tests/

README.md

.gitignore
```

Creating a Docker file

bash
```
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

build a docker file

bash
```
docker build -t feature-store-api -f docker/Dockerfile .
```
<img width="2940" height="1534" alt="image" src="https://github.com/user-attachments/assets/da69df3c-1cd2-42b0-907d-ae6368053f23" />

run a container

bash
```
docker run -p 8000:8000 feature-store-api
```
<img width="2896" height="338" alt="image" src="https://github.com/user-attachments/assets/64aaeeb9-fd69-4354-a851-91adc8245d7e" />

<img width="1912" height="190" alt="image" src="https://github.com/user-attachments/assets/ddd21edd-8a5d-4db8-a075-0c05aa236d38" />

The problem is that Redis is an external dependency. In production, we don't start services manually—we orchestrate them.

# Docker Compose

 bash
 ```
 version: "3.9"

services:

  redis:
    image: redis:7-alpine
    container_name: feast-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

  api:
    build:
      context: ../..
      dockerfile: docker/Dockerfile

    container_name: feature-store-api

    depends_on:
      - redis

    ports:
      - "8000:8000"

    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379

    volumes:
      - ../../:/app
 ```

 build

 bash
 ```
 docker compose -f deployments/docker/docker-compose.yml build
 ```

 Start the stack

 bash
 ```
docker compose -f deployments/docker/docker-compose.yml up
 ```
<img width="2940" height="1080" alt="image" src="https://github.com/user-attachments/assets/92b4e9d5-e0d3-4819-988e-2e7ec5d31a6b" />

<img width="2940" height="1624" alt="image" src="https://github.com/user-attachments/assets/5b265362-f93c-435e-bafb-e7548dadc253" />

still we are pointing to localhost in feature_store

updating feature_store.yaml

bash
```
online_store:
  type: redis
  connection_string: redis:6379
```

# Rebuild the image and up the container

bash
```
docker compose -f deployments/docker/docker-compose.yml down

docker compose -f deployments/docker/docker-compose.yml build --no-cache

docker compose -f deployments/docker/docker-compose.yml up
```

Now test the APi

<img width="2940" height="262" alt="image" src="https://github.com/user-attachments/assets/18d49de2-7748-423c-90de-03ca64130fc9" />

WE CAN SEE NULL VALUES we haven't copied to redis ( we haven't materialize the features

<img width="2382" height="298" alt="image" src="https://github.com/user-attachments/assets/f8c8f842-fe75-4c86-8752-0cf2fb8e53e2" />

lets materialize 

bash
```
docker exec -it feature-store-api sh

feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```
<img width="2110" height="292" alt="image" src="https://github.com/user-attachments/assets/e463d53c-cc4e-461b-87d2-778311b7bb54" />

docker container not able to access the features in mac, so we rebuild those inside the container

bash
```
docker exec -it feature-store-api sh

feast apply

feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

<img width="2360" height="1446" alt="image" src="https://github.com/user-attachments/assets/5f8eb9e6-58d1-4f3a-b256-905b66e7eacc" />

<img width="2914" height="884" alt="image" src="https://github.com/user-attachments/assets/74e90fd5-f636-46f3-91eb-d8e6477f05c8" />

# Production Configuration Management

bash
```
pip install pydantic-settings

pip freeze > requirements.txt

```

app/core/settings.py

bash
```
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Feature Store API"

    feature_store_repo: str = "."

    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
```

create .env

bash
```
APP_NAME=Feature Store API

FEATURE_STORE_REPO=.

LOG_LEVEL=INFO
```

# Structured Logging

## Install logging library

bash
```
pip install python-json-logger

pip freeze > requirements.txt
```

create app/core/logging.py

bash
```
import logging
import sys

from pythonjsonlogger import jsonlogger

from app.core.settings import settings


def setup_logging():
    logger = logging.getLogger()

    logger.setLevel(settings.log_level)

    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
```

Update app/main.py

add
bash
```
from app.core.logging import setup_logging
setup_logging()
```

Add Request Logging Middleware

app/core/middleware.py

bash
```
import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": duration_ms,
        },
    )

    response.headers["X-Request-ID"] = request_id

    return response
```
Register the middleware

app/main.py

add

bash
```
from app.core.middleware import log_requests

app.middleware("http")(log_requests)
```
Log business events

app/services/prediction_service.py

bash
```
from app.services.feast_service import get_customer_features
from app.models.dummy_model import predict
import logging

logger = logging.getLogger(__name__)

logger.info(
    "Fetching customer features",
    extra={"customer_id": customer_id},
)

def predict_customer(customer_id: int):
    features = get_customer_features(customer_id)
    label, probability = predict(features)
     logger.info(
    "Prediction generated",
    extra={
        "customer_id": customer_id,
        "prediction": prediction,
    },
)
    return {
        "customer_id": customer_id,
        "prediction": label,
        "probability": probability,
        "features": features,
    }
```

# Production Docker Image

Current Dockerfile  works, but it has several production issues:

Runs as the root user.
No health check.
Larger image than necessary.
Less secure.

## Multi stage docker Build

  bash
  ```
# ---------- Builder Stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Runtime Stage ----------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

COPY . .

RUN useradd -m appuser

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
  ```

  build and test the image

  bash
  ```
  docker build -t feature-store-api:prod -f docker/Dockerfile .

  docker compose -f deployments/docker/docker-compose.yml up --build
  ```

<img width="2940" height="352" alt="image" src="https://github.com/user-attachments/assets/8b6fe88e-b0b1-4b75-bed7-80e99d149386" />

 
<img width="2940" height="1584" alt="image" src="https://github.com/user-attachments/assets/f37de0c9-ff5e-4d9e-b669-4e735b8af6ba" />

# Testing the model


Installing test dependencies

bash
```
pip install pytest pytest-cov httpx pytest-mock

pip freeze > requirements.txt
```

## unit testing 

bash
```
from app.models.dummy_model import predict


def test_predict_returns_valid_response():
    features = {
        "age": 30,
        "salary": 75000,
        "total_spend": 20000,
    }

    prediction, probability = predict(features)

    assert prediction in ["High Value", "Low Value"]
    assert 0.0 <= probability <= 1.0
```

pytest.ini

bash
```
[pytest]
pythonpath = .
testpaths = Tests
```
This test verifies that your model returns a valid prediction and a probability in the expected range.

Test the model

bash
```
pytest Tests/unit/test_dummy_model.py -v
```

<img width="2926" height="812" alt="image" src="https://github.com/user-attachments/assets/6b1e5377-0dd8-4a00-8738-15280eedb111" />

# Mocking External Dependencies

Tests/unit/test_prediction_service.py

bash
```
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
```
test the mock
<img width="2940" height="1090" alt="image" src="https://github.com/user-attachments/assets/53afb122-aba3-4743-9688-3f3a41cd0d3a" />


# Integration testing

Tests/integration/test_api.py

bash
```
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
```
<img width="2938" height="1522" alt="image" src="https://github.com/user-attachments/assets/8bd573ea-1bbe-42e1-82bd-52ee344df70b" />

# Test report

bash
```
pytest --cov=app --cov-report=term-missing
```

<img width="2940" height="1360" alt="image" src="https://github.com/user-attachments/assets/efdf631b-75d5-4d8a-b5a7-52c22f84558a" />

# Container Registry (Amazon ECR)

bash
```
aws ecr create-repository \
    --repository-name feature-store-api \
    --region ap-south-1
```

<img width="2940" height="962" alt="image" src="https://github.com/user-attachments/assets/5fcf1bf2-bc1c-46ba-afd1-df28709d7629" />

Authenticate Docker to ECR

bash
```
aws ecr get-login-password \
    --region ap-south-1 | docker login \
    --username AWS \
    --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

Build the image

bash
```
docker build -t feature-store-api:1.0 -f docker/Dockerfile .
```

push the image

bash
```
docker push \
<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/feature-store-api:1.0
```

<img width="2934" height="790" alt="image" src="https://github.com/user-attachments/assets/23262744-5682-41d3-bb20-66582b46b025" />


# Deploy the Application to EKS

create a namespace

bash
```
apiVersion: v1
kind: Namespace
metadata:
  name: feature-store
```

deploy redis

bash
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: feature-store
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis

  template:
    metadata:
      labels:
        app: redis

    spec:
      containers:
      - name: redis
        image: redis:7-alpine

        ports:
        - containerPort: 6379

        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"

          limits:
            cpu: "500m"
            memory: "512Mi"
```

exposing redis

bash
```
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: feature-store

spec:
  selector:
    app: redis

  ports:
  - port: 6379
    targetPort: 6379

  type: ClusterIP
```

<img width="2496" height="660" alt="image" src="https://github.com/user-attachments/assets/a446b4f2-25c7-4579-bd68-fd66a6b21f53" />


api deployment

bash
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: feature-store-api
  namespace: feature-store
spec:
  replicas: 2
  revisionHistoryLimit: 5

  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1

  selector:
    matchLabels:
      app: feature-store-api

  template:
    metadata:
      labels:
        app: feature-store-api

    spec:
      containers:
      - name: feature-store-api
        image: 497508796460.dkr.ecr.ap-south-1.amazonaws.com/feature-store-api:1.0
        imagePullPolicy: Always

        ports:
        - containerPort: 8000

        env:
        - name: PYTHONUNBUFFERED
          value: "1"

        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"

          limits:
            cpu: "1000m"
            memory: "1Gi"

        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10

        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 20
```
got image pull back off

<img width="2768" height="326" alt="image" src="https://github.com/user-attachments/assets/0deb2b95-1457-477b-9b73-14189703e6df" />

Your EKS worker nodes are:

Amazon EC2 (t3.medium)
linux/amd64

So your image in ECR is an ARM64 image, but the EKS nodes are trying to pull an AMD64 image. They can't find one in the manifest,

rebuild for supported architecture

bash
```
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t 497508796460.dkr.ecr.ap-south-1.amazonaws.com/feature-store-api:1.0 \
  -f docker/Dockerfile \
  --push .
```

restart the deployment

bash
```
kubectl rollout restart deployment feature-store-api -n feature-store
```
<img width="2934" height="600" alt="image" src="https://github.com/user-attachments/assets/7836c803-ffda-412d-a966-b84238d6070b" />

<img width="2936" height="840" alt="image" src="https://github.com/user-attachments/assets/8e950875-8935-4d6d-a076-4429c56e3c4b" />

Port Forward the API

bash
```
kubectl port-forward svc/feature-store-api 8000:80 -n feature-store
```

<img width="2940" height="564" alt="image" src="https://github.com/user-attachments/assets/9a564ce0-8e9a-4f62-b23c-eb9b2cab102d" />

# OIDC provider

bash
```
eksctl utils associate-iam-oidc-provider \
  --cluster feature-store-lab \
  --region ap-south-1 \
  --approve
```

download an IAM policy

bash
```
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
```

create a IAM poicy

bash
```
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

Create the IAM Service Account (IRSA)

bash
```
eksctl create iamserviceaccount \
  --cluster feature-store-lab \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn arn:aws:iam::497508796460:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve \
  --region ap-south-1
```

adding helm repositories

bash
```
helm repo add eks https://aws.github.io/eks-charts

helm repo update
```

Installing aws load balncer controller

bash
```
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=feature-store-lab \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=ap-south-1 \
  --set vpcId=vpc-0c4c2c62047b7eab1
```

<img width="2938" height="874" alt="image" src="https://github.com/user-attachments/assets/44459e12-f801-4830-aa7a-e74fb69f84b0" />

verfiy the installation

<img width="2850" height="220" alt="image" src="https://github.com/user-attachments/assets/b430630d-2b86-4934-9cfe-6cbea4a15700" />

Once the controller is Running, we'll create a Kubernetes Ingress resource. AWS will automatically provision an Application Load Balancer (ALB) and expose your FastAPI service to the internet.


feature-store-ingress.yaml

bash
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: feature-store-ingress
  namespace: feature-store
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80}]'
    alb.ingress.kubernetes.io/success-codes: "200"
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: feature-store-api
                port:
                  number: 80
```

deploy and verify 

<img width="2940" height="350" alt="image" src="https://github.com/user-attachments/assets/e62672da-c121-4f6c-866c-7e00413c3d89" />

# CI/CD 

ery push to main will:

✅ Run unit tests
✅ Build a Docker image
✅ Tag the image with the Git commit SHA
✅ Push it to Amazon ECR
✅ Update the deployment image
✅ Roll out the new version on EKS
✅ Verify the rollout succeeded


create  a trust policy 

bash
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::497508796460:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:kornurabindranath-ctrl/MLOPS:*"
        }
      }
    }
  ]
}
```

create Iam Role

bash
```
aws iam create-role \
  --role-name GitHubActionsEKSRole \
  --assume-role-policy-document file://github-trust-policy.json
```

Attach permissions

bash
```
aws iam attach-role-policy \
  --role-name GitHubActionsEKSRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser

aws iam attach-role-policy \
  --role-name GitHubActionsEKSRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
```

get role arn

bash
```
aws iam get-role \
  --role-name GitHubActionsEKSRole \
  --query "Role.Arn" \
  --output text
```

# build the GitHub Actions pipeline.

bash
```
name: Feature Store CI/CD

on:
  push:
    branches:
      - main

env:
  AWS_REGION: ap-south-1
  ECR_REPOSITORY: feature-store-api
  CLUSTER_NAME: feature-store-lab

permissions:
  id-token: write
  contents: read

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: <ROLE_ARN>
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Tests
        run: |
          pytest Tests/

      - name: Build Docker Image
        run: |
          docker build \
            -f docker/Dockerfile \
            -t $ECR_REPOSITORY:${{ github.sha }} \
            .

      - name: Tag Image
        run: |
          docker tag \
          $ECR_REPOSITORY:${{ github.sha }} \
          497508796460.dkr.ecr.ap-south-1.amazonaws.com/$ECR_REPOSITORY:${{ github.sha }}

      - name: Push Image
        run: |
          docker push \
          497508796460.dkr.ecr.ap-south-1.amazonaws.com/$ECR_REPOSITORY:${{ github.sha }}

      - name: Configure kubectl
        run: |
          aws eks update-kubeconfig \
            --name $CLUSTER_NAME \
            --region $AWS_REGION

      - name: Deploy
        run: |
          kubectl set image deployment/feature-store-api \
          feature-store-api=497508796460.dkr.ecr.ap-south-1.amazonaws.com/$ECR_REPOSITORY:${{ github.sha }} \
          -n feature-store

      - name: Verify Rollout
        run: |
          kubectl rollout status deployment/feature-store-api \
          -n feature-store
```

# Argo CD GitOps

bash
```
kubectl create namespace argocd
```

Installing argocd

bash
```
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

verfiy the installation

<img width="2714" height="510" alt="image" src="https://github.com/user-attachments/assets/2dbfdaf9-da9c-4af1-92e5-4cd400480c6e" />


# port forward 

bash
```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

get the password

bash
```
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 --decode
echo
```

create an argo CD application

bash
```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: feature-store
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/kornurabindranath-ctrl/MLOPS.git
    targetRevision: main
    path: Usecase-1-Feature-Store-Feast/k8s

  destination:
    server: https://kubernetes.default.svc
    namespace: feature-store

  syncPolicy:
    automated:
      prune: true
      selfHeal: true

    syncOptions:
    - CreateNamespace=true
```

verfiy
bash
```
kubectl get applications -n argocd
```

<img width="2904" height="202" alt="image" src="https://github.com/user-attachments/assets/44a20876-221a-49ab-9095-954b7fc782ba" />


Now chnage deployment replicas from 2 to 4 
 then commit

 bash
 ```
 git add .
git commit -m "Scale API to 4 replicas"
git push origin main
 ```



<img width="2892" height="294" alt="image" src="https://github.com/user-attachments/assets/e2b368b0-9aef-4277-b057-33d17fdda78c" />

# Observability with Prometheus

bash
```
kubectl create namespace monitoring
```

Add Helm repo for prom

bash
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update
```

## Install kube-prometheus-stack

bash
```
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring

```

<img width="2940" height="1562" alt="image" src="https://github.com/user-attachments/assets/1aca66c9-e450-4eb1-80cd-e44501d23980" />

verify

<img width="2782" height="476" alt="image" src="https://github.com/user-attachments/assets/ac7a673c-4e01-4890-9c09-e50fc6e0206b" />


port forward grafana

<img width="2922" height="1692" alt="image" src="https://github.com/user-attachments/assets/9be3ef50-82c9-4f33-ac57-2332ebe33cf6" />

These dashboards will already show metrics from your EKS cluster.



<img width="2934" height="1224" alt="image" src="https://github.com/user-attachments/assets/8f834ccf-741a-4c4c-bb5b-6a397b62faba" />

bash
```
kubectl port-forward svc/feature-store-api 8000:80 -n feature-store

```



we don't have custome metrics from the application

<img width="2216" height="214" alt="image" src="https://github.com/user-attachments/assets/bcab7839-8bfe-4b63-bb62-28a594da394b" />

# Instrument the FastAPI application

bash
```
pip install prometheus-fastapi-instrumentator
```

prometheus-fastapi-instrumentator

It automatically exposes:

HTTP request count
Request latency
Response size
Status codes
Requests in progress
Python process metrics

This is the library commonly used with FastAPI.

<img width="2934" height="1428" alt="image" src="https://github.com/user-attachments/assets/edb763e2-30ea-4146-9cc3-ddf2f5e4a5cb" />

# Create a ServiceMonitor

Prometheus doesn't automatically scrape every service. The kube-prometheus-stack uses a ServiceMonitor Custom Resource to discover applications


bash
```
kubectl get svc -n feature-store -o yaml
```
 need to get pots and service name and labels so that we can use on the service monitor


 bash
 ```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: feature-store-api
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: feature-store-api
  namespaceSelector:
    matchNames:
      - feature-store
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
 ```

verfiy prom is scraping the metrics

bash
```
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090
```

<img width="2938" height="1470" alt="image" src="https://github.com/user-attachments/assets/8b9e5042-71cb-4472-8117-289ac22324ad" />

bash
```
kubectl port-forward svc/feature-store-api -n feature-store 8000:80
```

<img width="2938" height="1558" alt="image" src="https://github.com/user-attachments/assets/d01d4e5c-d326-4a24-b6b4-e82d41ee0c70" />

<img width="2940" height="1532" alt="image" src="https://github.com/user-attachments/assets/40c64f1e-591d-4971-b95d-7f019eebe4d4" />

validate the grafana

bash
```
kubectl port-forward svc/monitoring-grafana \
-n monitoring 3000:80
```

<img width="2906" height="1706" alt="image" src="https://github.com/user-attachments/assets/8e6d4303-a3b2-417c-9a38-bc644ab9a55f" />

Panel	Visualization	Query
Total Requests	Stat	sum(http_requests_total)
Requests/sec	Time series	sum(rate(http_requests_total[1m]))
Avg Response Time	Time series	sum(rate(http_request_duration_seconds_sum[1m])) / sum(rate(http_request_duration_seconds_count[1m]))
CPU Usage	Time series	rate(process_cpu_seconds_total[1m])
Memory Usage (MiB)	Time series	process_resident_memory_bytes / 1024 / 1024
Requests by Endpoint	Time series	sum by (handler)(rate(http_requests_total[1m]))
Requests by Status	Time series	sum by (status)(rate(http_requests_total[1m]))


# Kubernetes Horizontal Pod Autoscaler (HPA)





