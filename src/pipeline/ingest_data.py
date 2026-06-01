import csv
from pathlib import Path
import sqlite3

# 1. Setup smart paths (Aligned perfectly to the left)
base_dir = Path(__file__).resolve().parent.parent.parent
clean_path = base_dir / "clean_transactions.csv"
db_path = base_dir / "fintech_vault.db"

# 2. Connect to the database vault
connection = sqlite3.connect(str(db_path))
cursor = connection.cursor()

# 3. Open our clean CSV file using our smart path variable
with open(clean_path, mode="r") as file:
    csv_reader = csv.DictReader(file)
    

    print("--- Starting Data Ingestion ---")

    # 3. Loop through each clean row
    for row in csv_reader:
        user = row["user_id"]
        amount = float(row["amount"])  # Ensure the amount is treated as a decimal number
        location = row["location"]

        # 4. Insert this specific row into our SQL table
        # We use '?' placeholders to securely pass data into SQL
        cursor.execute(
            """
            INSERT INTO transactions (user_id, amount, location, is_fraud)
            VALUES (?, ?, ?, 0)
        """,
            (user, amount, location),
        )

        print(f"Successfully loaded: User {user} | ${amount} | {location}")

# 5. Save (commit) all the insertions and close the connection
connection.commit()
connection.close()

print("\n🎉 All clean data has been successfully pushed into the database vault!")