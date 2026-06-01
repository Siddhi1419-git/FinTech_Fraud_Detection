import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = os.path.join(base_dir, "fintech_vault.db")

connection = sqlite3.connect(str(db_path))
cursor = connection.cursor()

print("--- 🏗️ Initializing Feature Store Table 🏗️ ---")

# 2. Create the user_profiles table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY,
    total_transactions INTEGER,
    total_spent REAL,
    average_ticket REAL
)
""")
connection.commit()

print("Table 'user_profiles' is ready.")

# 3. Fetch the raw aggregates from our transactions table
cursor.execute("""
SELECT 
    user_id, 
    COUNT(transaction_id),
    SUM(amount)
FROM transactions
GROUP BY user_id;
""")
analytics_results = cursor.fetchall()

print("\n--- 💾 Saving Engineered Features to Database 💾 ---")

# 4. Loop through the calculations and store them permanently
for row in analytics_results:
    user = row[0]
    tx_count = row[1]
    total_spent = row[2]
    average_ticket = total_spent / tx_count if tx_count > 0 else 0.0
    
    # INSERT OR REPLACE handles updating existing records cleanly
    cursor.execute("""
    INSERT OR REPLACE INTO user_profiles (user_id, total_transactions, total_spent, average_ticket)
    VALUES (?, ?, ?, ?)
    """, (user, tx_count, total_spent, average_ticket))
    
    print(f"Saved profile for {user} -> Avg Swipe: ${average_ticket:.2f}")

# Save changes and close connection
connection.commit()
connection.close()

print("\n🎉 Feature Store update complete! Profiles are permanently stored.")