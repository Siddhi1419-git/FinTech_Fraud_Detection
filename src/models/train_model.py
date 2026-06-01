import pickle
from pathlib import Path
import pandas as pd
import numpy as np
import sqlite3

# Advanced ML Toolkit
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "fintech_vault.db"
MODEL_PATH = BASE_DIR / "src" / "models" / "fraud_tree_model.pkl"

print("🧠 Loading behavioral feature matrices from feature store...")

# 1. Fetch features from SQLite profile vault
connection = sqlite3.connect(str(DB_PATH))
df = pd.read_sql_query("SELECT * FROM user_profiles", connection)
connection.close()

# Define features and engineer a synthetic ground-truth target label for demonstration
X = df[["transaction_count", "total_spent", "average_ticket"]].values
# Create a binary label: 1 if average ticket or total spent is anomalously high (Fraud simulation)
y = np.where((df["average_ticket"] > 450) | (df["total_spent"] > 10000), 1, 0)

# Check class distribution
fraud_count = np.sum(y)
normal_count = len(y) - fraud_count
print(f"📊 Original Dataset Shape -> Normal: {normal_count}, Fraudulent (Anomalies): {fraud_count}")

# 2. Split into Train/Test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_test_split=0.2, random_state=42, stratify=y)

# 3. Handle Class Imbalance using SMOTE
print("⚖️ Applying SMOTE over-sampling to balance the minority fraud class...")
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
print(f"📈 Balanced Training Shape -> Normal: {np.sum(y_train_balanced==0)}, Fraudulent: {np.sum(y_train_balanced==1)}")

# 4. Initialize and Train Competitor Models
print("\n⚔️ Training Competitor Classifiers...")
dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train_balanced, y_train_balanced)

xgb_model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42, eval_metric="logloss")
xgb_model.fit(X_train_balanced, y_train_balanced)

# 5. Evaluate and Compare Metrics
models_report = {}
for name, model in [("Decision Tree", dt_model), ("XGBoost (Production)", xgb_model)]:
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    models_report[name] = {
        "Precision": precision_score(y_test, preds, zero_division=0),
        "Recall": recall_score(y_test, preds, zero_division=0),
        "F1-Score": f1_score(y_test, preds, zero_division=0),
        "AUC-ROC": roc_auc_score(y_test, probs)
    }

# 6. Display Performance Evaluation Matrix
print("\n=========================================================================")
print("🏆 FINAL MODEL EVALUATION MATRIX (CLASS-IMBALANCE ADJUSTED)")
print("=========================================================================")
report_df = pd.DataFrame(models_report).T
print(report_df.to_string(formatters={
    "Precision": "{:,.2f}".format,
    "Recall": "{:,.2f}".format,
    "F1-Score": "{:,.2f}".format,
    "AUC-ROC": "{:,.2f}".format
}))
print("=========================================================================\n")

# 7. Export the Champion Model (XGBoost) to storage
print(f"💾 Freezing production champion model artifact to: {MODEL_PATH.name}")
with open(MODEL_PATH, "wb") as file:
    pickle.dump(xgb_model, file)

print("✅ Model evaluation phase successfully complete.")