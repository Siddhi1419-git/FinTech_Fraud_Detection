from pathlib import Path
import pickle
import numpy as np

# 1. Locate our saved AI brain file securely
base_dir = Path(__file__).resolve().parent.parent.parent
model_path = base_dir / "src" / "models" / "fraud_tree_model.pkl"

print("--- 🧠 Loading AI Model Brain from Storage... ---")

# 2. Load the binary model artifact back into active memory
with open(model_path, "rb") as file:
    ai_model = pickle.load(file)

print("✅ AI Model Loaded and Operational.\n")
print("--- 💸 Screening Incoming Live User Profiles 💸 ---\n")

# 3. Simulate incoming data for two new distinct users who just signed up
# Data order matches our features: [Total Transactions, Total Spent, Average Ticket]
new_users = {
    "user_201 (New Student Account)": np.array([[3, 45.00, 15.00]]),
    "user_202 (Suspicious High Volume)": np.array([[12, 14500.00, 1208.33]])
}

# 4. Run the data through our AI flowchart
for username, profile_data in new_users.items():
    # Pass features to the model to get a raw prediction (0 or 1)
    prediction = ai_model.predict(profile_data)
    
    # Extract confidence probabilities (how sure the AI is about its decision)
    probabilities = ai_model.predict_proba(profile_data)[0]
    fraud_probability = probabilities[1] * 100
    
    print(f"👤 Evaluating: {username}")
    print(f"   ↳ Input Features: {profile_data[0].tolist()}")
    print(f"   ↳ AI Fraud Confidence: {fraud_probability:.1f}%")
    
    if prediction[0] == 1:
        print("   🚨 AI DECISION: HIGH RISK FRAUD PATTERN DETECTED - LOCK ACCOUNT")
    else:
        print("   ✅ AI DECISION: BEHAVIOR PROFILE SECURE - PASS")
        
    print("-" * 65)