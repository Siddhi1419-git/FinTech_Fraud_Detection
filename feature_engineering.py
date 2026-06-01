import sqlite3

# 1. Connect to our database vault
connection = sqlite3.connect("fintech_vault.db")
cursor = connection.cursor()

print("--- 🧠 Running Advanced Behavioral Analytics 🧠 ---\n")

# 2. Advanced SQL Query to calculate Count and Sum
query = """
SELECT 
    user_id, 
    COUNT(transaction_id) AS total_transactions,
    SUM(amount) AS total_amount_spent
FROM transactions
GROUP BY user_id;
"""

cursor.execute(query)
analytics_results = cursor.fetchall()

# Keep track of high-risk users
flagged_users = 0

# 3. Process each user profile
for row in analytics_results:
    user = row[0]
    tx_count = row[1]
    total_spent = row[2]
    
    # 4. Calculate the Average Transaction Size
    # We protect against division by zero just in case
    if tx_count > 0:
        average_ticket = total_spent / tx_count
    else:
        average_ticket = 0.0
        
    print(f"👤 User: {user}")
    print(f"   ↳ Activity: {tx_count} transactions")
    print(f"   ↳ Avg Ticket Size: ${average_ticket:.2f}")
    
    # 5. Behavioral Rule: Flag users with an unusually high average swipe size
    if average_ticket > 500.00:
        print(f"   🚨 STATUS: FLAGGED - High Average Ticket Size!")
        flagged_users += 1
    else:
        print(f"   ✅ STATUS: Clear")
        
    print("-" * 45)

print(f"\n🏁 Analytics Scan Complete. Flagged {flagged_users} high-risk user profiles.")

# Close connection safely
connection.close()