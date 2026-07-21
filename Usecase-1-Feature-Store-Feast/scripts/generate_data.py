from pathlib import Path
from faker import Faker
import pandas as pd
import random

# -----------------------------
# Configuration
# -----------------------------

fake = Faker()

NUM_CUSTOMERS = 10_000
NUM_TRANSACTIONS = 100_000

CITIES = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata",
]

MERCHANTS = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Uber",
    "Apple",
    "Reliance",
    "DMart",
]

CATEGORIES = [
    "Shopping",
    "Food",
    "Travel",
    "Electronics",
    "Groceries",
]

# -----------------------------
# Directories
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Generate Customers
# -----------------------------

print("Generating customers...")

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):
    customers.append(
        {
            "customer_id": customer_id,
            "name": fake.name(),
            "age": random.randint(18, 70),
            "city": random.choice(CITIES),
            "salary": random.randint(30_000, 250_000),
            "event_timestamp": fake.date_time_between(
             start_date="-365d",
             end_date="now",
    ),
        }
    )

customers_df = pd.DataFrame(customers)

customers_file = DATA_DIR / "customers.csv"

customers_df.to_csv(
    customers_file,
    index=False,
)

print(f"Created: {customers_file}")

# -----------------------------
# Generate Transactions
# -----------------------------

print("Generating transactions...")

transactions = []

for transaction_id in range(1, NUM_TRANSACTIONS + 1):
    transactions.append(
        {
            "transaction_id": transaction_id,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "amount": round(random.uniform(50, 15000), 2),
            "merchant": random.choice(MERCHANTS),
            "category": random.choice(CATEGORIES),
            "timestamp": fake.date_time_between(
                start_date="-365d",
                end_date="now",
            ),
        }
    )

transactions_df = pd.DataFrame(transactions)

transactions_file = DATA_DIR / "transactions.csv"

transactions_df.to_csv(
    transactions_file,
    index=False,
)

print(f"Created: {transactions_file}")
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
# -----------------------------
# Summary
# -----------------------------

print("\n===================================")
print("Data generation completed!")
print("===================================")
print(f"Customers     : {len(customers_df):,}")
print(f"Transactions  : {len(transactions_df):,}")
print(f"Output Folder : {DATA_DIR}")
print("===================================")
