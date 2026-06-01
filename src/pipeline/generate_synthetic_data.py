import csv
from datetime import datetime, timedelta
import random
from pathlib import Path

# 1. Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
output_file = BASE_DIR / "raw_transactions.csv"

# Configuration parameters
NUM_RECORDS = 1200
START_DATE = datetime(2026, 1, 1)

merchants = {
    "Retail": ["Amazon", "Walmart", "Target", "BestBuy"],
    "Grocery": ["Kroger", "WholeFoods", "Safeway"],
    "Entertainment": ["Netflix", "Spotify", "Steam", "Cinema"],
    "Dining": ["Starbucks", "McDonalds", "Chipotle", "UberEats"],
    "Travel": ["Uber", "Delta Air", "Airbnb", "Shell Gas"]
}

# Standard domestic locations for normal transactions
domestic_locations = ["Patna", "Mumbai", "Delhi", "Bangalore", "Online"]

print(f"🏭 Manufacturing {NUM_RECORDS} realistic synthetic financial logs (with locations)...")

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Added "location" to the headers to satisfy clean_data.py 🛡️
    writer.writerow(["user_id", "amount", "timestamp", "merchant", "location"])
    
    for i in range(NUM_RECORDS):
        user_id = f"USR_{random.randint(100, 150):03d}"
        
        category = random.choice(list(merchants.keys()))
        merchant = random.choice(merchants[category])
        location = random.choice(domestic_locations)
        
        random_minutes = random.randint(0, 43200) 
        tx_time = START_DATE + timedelta(minutes=random_minutes)
        timestamp_str = tx_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if category == "Grocery":
            amount = round(random.uniform(20.00, 180.00), 2)
        elif category == "Dining":
            amount = round(random.uniform(5.50, 65.00), 2)
        elif category == "Entertainment":
            amount = round(random.uniform(9.99, 50.00), 2)
        else:
            amount = round(random.uniform(15.00, 300.00), 2)
            
        # 🚨 Inject Hidden Fraud Anomalies (approx 3% of data)
        if random.random() < 0.03:
            amount = round(random.uniform(600.00, 5000.00), 2)
            merchant = "Unknown_Overseas_Vendor"
            location = "International"  # Highly suspicious location mismatch anomaly!
            
        writer.writerow([user_id, amount, timestamp_str, merchant, location])

print(f"✅ Success! Overwrote '{output_file.name}' with a rich, location-aware dataset.")