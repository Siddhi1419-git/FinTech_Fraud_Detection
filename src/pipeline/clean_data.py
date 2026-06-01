from pathlib import Path
import csv

base_dir = Path(__file__).resolve().parent.parent.parent
raw_path = base_dir / "raw_transactions.csv"
clean_path = base_dir / "clean_transactions.csv"

with open(raw_path, mode="r") as infile, open(
    clean_path, mode="w", newline=""
) as outfile:

    reader = csv.DictReader(infile)

    # Define the columns for our new, clean file
    fieldnames = ["user_id", "amount", "location"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Writes the top row (headers)

    print("--- Starting Data Cleaning Process ---")

    for row in reader:
        user = row["user_id"]
        amount_raw = row["amount"]
        location_raw = row["location"]

        # --- FILTER 1: Fix the accidental spaces in Location ---
        # .strip() automatically cuts off spaces from the beginning and end
        location = location_raw.strip()

        # --- FILTER 2: Handle the missing amount (user_104) ---
        if amount_raw == "":
            print(f"⚠️ Warning: Found missing amount for {user}. Setting to 0.0")
            amount = 0.0
        else:
            # Convert text to a decimal number
            amount = float(amount_raw)

        # --- FILTER 3: Fix the negative amount (user_105) ---
        # abs() stands for "absolute value". It turns negative numbers into positive numbers!
        if amount < 0:
            print(f"⚠️ Warning: Found negative amount ({amount}) for {user}. Fixing to positive.")
            amount = abs(amount)

        # 2. Write the freshly cleaned row into our new file
        writer.writerow({"user_id": user, "amount": amount, "location": location})

print("\n🎉 Data cleaning complete! Saved as 'clean_transactions.csv'")