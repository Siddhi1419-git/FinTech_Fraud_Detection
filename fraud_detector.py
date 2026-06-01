import sqlite3

# 1. Connect to our database vault
connection = sqlite3.connect("fintech_vault.db")
cursor = connection.cursor()

print("--- 🛡️ Launching Fraud Detection Engine 🛡️ ---")

# 2. Fetch all transactions that are currently marked as safe (is_fraud = 0)
cursor.execute("SELECT transaction_id, user_id, amount, location FROM transactions WHERE is_fraud = 0")
safe_transactions = cursor.fetchall()

# Keep track of how many frauds we catch today
frauds_detected = 0

# 3. Loop through and evaluate each transaction
for row in safe_transactions:
    tx_id = row[0]
    user = row[1]
    amount = row[2]
    location = row[3]
    
    # 4. Apply our Security Rule: Is the amount greater than $1000?
    if amount > 1000.00:
        print(f"🚨 ALERT: Suspicious transaction detected! ID: {tx_id} | User: {user} | Amount: ${amount} | Location: {location}")
        
        # 5. Update this specific transaction in the database to mark it as Fraud (is_fraud = 1)
        cursor.execute(
            "UPDATE transactions SET is_fraud = 1 WHERE transaction_id = ?", 
            (tx_id,)
        )
        frauds_detected += 1

# 6. Save our changes to the database vault
connection.commit()

print("\n--- 🏁 Scan Complete ---")
print(f"Total transactions scanned: {len(safe_transactions)}")
print(f"Total fraudulent activities blocked and flagged: {frauds_detected}")

# Close the vault safely
connection.close()