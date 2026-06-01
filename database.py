import sqlite3

# 1. Connect to our existing vault
connection = sqlite3.connect("fintech_vault.db")
cursor = connection.cursor()

# 2. Insert Fake Transaction #1 (A normal grocery purchase)
cursor.execute(
    """
    INSERT INTO transactions (user_id, amount, location, is_fraud)
    VALUES ('user_101', 45.50, 'New York', 0)
"""
)

# 3. Insert Fake Transaction #2 (A highly suspicious large transfer)
cursor.execute(
    """
    INSERT INTO transactions (user_id, amount, location, is_fraud)
    VALUES ('user_102', 9999.99, 'Unknown Proxy', 1)
"""
)

# Save our inserts!
connection.commit()
print("Fake transactions inserted successfully!")

# 4. Now, let's ask the database to show us everything inside the table
cursor.execute("SELECT * FROM transactions")

# Fetch all the rows that the database found
all_transactions = cursor.fetchall()

print("\n--- Current Data in Vault ---")
# Loop through each row and print it beautifully
for row in all_transactions:
    print(
        f"ID: {row[0]} | User: {row[1]} | Amount: ${row[2]} | Location: {row[3]} | Is Fraud: {row[4]}"
    )

# Close the vault safely
connection.close()