
from pathlib import Path
import sqlite3

# This points to the exact same root directory file
base_dir = Path(__file__).resolve().parent.parent.parent
db_path = base_dir / "fintech_vault.db"

connection = sqlite3.connect(str(db_path))
cursor = connection.cursor()

print("--- 🎲 Evaluating Multi-Variable Risk Scores 🎲 ---\n")

# 2. Fetch our pre-calculated features from the Feature Store
cursor.execute("SELECT user_id, total_transactions, total_spent, average_ticket FROM user_profiles")
profiles = cursor.fetchall()

for row in profiles:
    user_id = row[0]
    tx_count = row[1]
    total_spent = row[2]
    avg_ticket = row[3]
    
    # Base risk score starts at 0
    risk_score = 0
    risk_reasons = []
    
    # Variable 1: Evaluate Frequency Risk (Max 40 points)
    if tx_count > 5:
        risk_score += 40
        risk_reasons.append("High Transaction Frequency")
    elif tx_count > 2:
        risk_score += 20
        risk_reasons.append("Moderate Transaction Frequency")
        
    # Variable 2: Evaluate Monetary Volume Risk (Max 60 points)
    if avg_ticket > 5000.00:
        risk_score += 60
        risk_reasons.append("Extreme Average Ticket Size")
    elif avg_ticket > 500.00:
        risk_score += 30
        risk_reasons.append("Elevated Average Ticket Size")

    # 3. Determine Account Security Status based on combined score
    if risk_score >= 70:
        status = "🔴 CRITICAL RISK - FREEZE ACCOUNT"
    elif risk_score >= 30:
        status = "🟡 MODERATE RISK - MONITOR ACTIVITY"
    else:
        status = "🟢 LOW RISK - SAFE"
        
    # 4. Display the comprehensive risk report
    print(f"👤 Account: {user_id}")
    print(f"   ↳ Behavioral Risk Score: {risk_score}/100")
    print(f"   ↳ Security Status: {status}")
    if risk_reasons:
        print(f"   ↳ Flags Triggered: {', '.join(risk_reasons)}")
    print("-" * 50)

# Close connection safely
connection.close()