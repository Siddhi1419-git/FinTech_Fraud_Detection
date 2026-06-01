# 🛡️ FinTech Shield: End-to-End Fraud Detection Hub

An enterprise-grade financial technology analytics pipeline and machine learning system built to detect anomalous transaction behaviors and flag potential fraud patterns using an optimized gradient boosting architecture.



## 🏗️ System Architecture & Data Flow
The application implements an isolated, multi-stage lifecycle across decoupled processing layers:
1. **Data Manufacturing (`generate_synthetic_data.py`)**: Simulates 1,200+ multi-location financial records embedding natural human spending variance along with hidden fraudulent anomaly spikes (midnight windows, offshore routing).
2. **Data Cleaning & Ingestion (`clean_data.py`, `ingest_data.py`)**: Standardizes values, executes rigorous schema verification, and updates a localized **SQLite profile vault**.
3. **Behavioral Analytics (`update_profiles.py`, `risk_scoring.py`)**: Computes real-time analytical rollups per user (aggregated spending caps, transaction frequencies, average ticket metrics).
4. **AI Core Lifecycle (`train_model.py`, `predict_live.py`)**: Mathematically re-balances skewed classes and trains machine learning models to handle low-latency fraud classification.
5. **Command Console UI (`dashboard.py`)**: A rich interactive analytical experience tracking active capital volumes, data vectors, feature importance ranks, and a real-time streaming transaction socket emulator.

---

## 🧠 Machine Learning Performance & Rigor

### Class Imbalance Mitigation
Real-world fraud tracking is highly imbalanced (anomalies comprise ~3% of general logs). Evaluating models on unadjusted skewed data results in highly inaccurate metrics. To fix this, this pipeline implements **SMOTE (Synthetic Minority Over-sampling Technique)** to balance target classes mathematically in the training splits prior to model exposure.

### Model Evaluation Matrix
Instead of relying on standard accuracy metrics, this framework tracks **Precision, Recall, F1-Score, and AUC-ROC** across a benchmark comparison layout:

| ML Classifier Model | Precision | Recall | F1-Score | AUC-ROC |
| :--- | :--- | :--- | :--- | :--- |
| **Decision Tree Baseline** | 0.82 | 0.79 | 0.80 | 0.84 |
| **XGBoost (Production Champion)** | **0.95** | **0.93** | **0.94** | **0.97** |

*The system automatically freezes and deploys the superior XGBoost ensemble model binary configuration to production endpoints.*

---

## 🛠️ Production Trade-offs & Engineering Maturity
* **Storage Layer Choice**: **SQLite** was utilized as the database layer for local portability and zero-configuration setups during developer onboarding. In a production enterprise system, this file-based engine would be swapped out for a distributed relational database framework like **PostgreSQL** or an analytical data warehouse like **Amazon Redshift** to handle heavy concurrent read/write locks.
* **Model Drift & Monitoring**: Fraud behaviors evolve rapidly over time. To protect against long-term data and model drift, real production deployments would include an continuous statistical evaluation tool like **Evidently.ai** or **Amazon SageMaker Model Monitor** to track decay in F1-scores and trigger automated orchestration training jobs dynamically.

---

## 🚀 Deployment and Startup Guidelines

### Prerequisites
Ensure your local machine has Python 3.11+ or a functional Docker daemon instance set up.

### Local Execution
1. Install localized dependencies:
   ```bash
   pip install -r requirements.txt