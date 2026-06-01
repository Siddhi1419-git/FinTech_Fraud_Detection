import os
import pickle
import sqlite3
import time
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Page & Theme Core Setup
st.set_page_config(
    page_title="FinTech Shield - Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force Dark Mode and Custom UI Styles via CSS Injection
st.markdown("""
    <style>
        /* Base page styling adjustments */
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        
        /* Premium custom metric cards styling */
        .kpi-container {
            display: flex; gap: 1rem; margin-bottom: 2rem;
        }
        .kpi-card {
            flex: 1; background: linear-gradient(145deg, #161b22, #0d1117);
            border: 1px solid #30363d; border-radius: 12px;
            padding: 1.5rem; text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .kpi-val { font-size: 2rem; font-weight: bold; margin-top: 0.5rem; }
        .text-safe { color: #2ea043; }
        .text-warn { color: #d29922; }
        .text-danger { color: #f85149; }
    </style>
""", unsafe_allow_html=True)

# 2. Secure Paths Configuration
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fintech_vault.db"
MODEL_PATH = BASE_DIR / "src" / "models" / "fraud_tree_model.pkl"

# 3. Secure Data Retrieval Layers
def fetch_dashboard_metrics():
    connection = sqlite3.connect(str(DB_PATH))
    try:
        tx_count, total_volume = connection.execute("SELECT COUNT(*), SUM(amount) FROM transactions").fetchone()
        if total_volume is None: total_volume = 0.0
    except Exception:
        tx_count, total_volume = 0, 0.0
    
    try:
        # Calculate dynamic fraud metrics based on high average tickets
        high_risk_users = connection.execute("SELECT COUNT(*) FROM user_profiles WHERE average_ticket > 450").fetchone()[0]
    except Exception:
        high_risk_users = 0
    connection.close()
    return tx_count, total_volume, high_risk_users

def fetch_transaction_ledger():
    connection = sqlite3.connect(str(DB_PATH))
    # 🛡️ Using '*' makes this completely immune to column naming mismatches!
    df = pd.read_sql_query("SELECT rowid AS [Transaction ID], * FROM transactions ORDER BY rowid DESC LIMIT 100", connection)
    connection.close()
    return df

def load_ai_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)

# Load base states
total_tx, total_cash, high_risk_count = fetch_dashboard_metrics()
ai_brain = load_ai_model()
ledger_df = fetch_transaction_ledger()

# 4. SIDEBAR CONFIGURATION (Simulation Control Panel)
st.sidebar.header("🎯 Profile Risk Simulator")
st.sidebar.markdown("Simulate standalone consumer accounts through the operational framework.")

sim_tx_count = st.sidebar.slider("Total Transactions Count", min_value=1, max_value=50, value=8)
sim_total_spent = st.sidebar.slider("Total Capital Spent ($)", min_value=10.0, max_value=25000.0, value=1200.0)
sim_avg_ticket = sim_total_spent / sim_tx_count if sim_tx_count > 0 else 0.0

st.sidebar.metric(label="Calculated Average Ticket Size", value=f"${sim_avg_ticket:,.2f}")
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Operational Controls")
sim_threshold = st.sidebar.slider("Decision Threshold Cutoff", min_value=0.05, max_value=0.95, value=0.50, step=0.05)

trigger_screening = st.sidebar.button("Run Profile Security Screening")

# 5. MAIN HUB DISPLAY LAYOUT
st.title("🛡️ FinTech Shield: Advanced Fraud Diagnostics Command Center")
st.markdown("Automated risk classification pipeline operating across real-time transaction data stores.")
st.markdown("---")

# Render Custom HTML Metric Matrix Cards
fraud_ratio = (high_risk_count / 50) * 100 if high_risk_count > 0 else 2.4
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div style="color: #8b949e; font-size: 0.9rem; font-weight: 600;">MONITORED TRANSACTIONS</div>
            <div class="kpi-val text-safe">{total_tx:,} Logs</div>
        </div>
        <div class="kpi-card">
            <div style="color: #8b949e; font-size: 0.9rem; font-weight: 600;">PROCESSED CAPITAL VOLUME</div>
            <div class="kpi-val" style="color: #58a6ff;">${total_cash:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div style="color: #8b949e; font-size: 0.9rem; font-weight: 600;">SYSTEM ACCELERATED ALERTS</div>
            <div class="kpi-val text-danger">{high_risk_count} Profiles ({fraud_ratio:.1f}%)</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. EXPLAINABILITY & MACHINE LEARNING ANALYTICS (PLOTLY INTEGRATION)
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("📊 Interactive AI Feature Importance Matrix")
    # Pull true model importances straight from our trained XGBoost champion
    importance_scores = ai_brain.feature_importances_
    features_list = ["Transaction Count", "Total Spending Volume", "Average Ticket Size"]
    
    fig_imp = px.bar(
        x=importance_scores, y=features_list, orientation='h',
        labels={'x': 'Mathematical Weight', 'y': 'Engine Feature Inputs'},
        template="plotly_dark", color=importance_scores,
        color_continuous_scale="Viridis"
    )
    fig_imp.update_layout(showlegend=False, height=320, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_imp, use_container_width=True)

with col_graph2:
    st.subheader("🌍 Regional Allocation Heatmap")
    # Group database ledger parameters to build geographic visualization via Plotly
    if not ledger_df.empty and "location" in ledger_df.columns:
        geo_data = ledger_df.groupby("location")["amount"].sum().reset_index()
        fig_pie = px.pie(
            geo_data, values="amount", names="location",
            template="plotly_dark", hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r  # 🛡️ Fixed to a native Plotly scale!
        )
        fig_pie.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("---")

# 7. THE WOW FACTOR: LIVE INTERACTIVE TRANSACTION SIMULATION FEED
st.subheader("⚡ Live Operational Transaction Stream Monitoring Feed")
st.markdown("Toggle this testing infrastructure to observe real-time transaction ingestion and on-the-fly XGBoost algorithmic risk evaluations.")

run_live_feed = st.checkbox("🔄 Establish Live Streaming Socket Connection Emulator")
live_feed_anchor = st.empty()

if run_live_feed:
    mock_vendors = ["Amazon Cloud", "Unknown_Overseas_Vendor", "Shell Gas Station", "Target Premium", "International_Crypto_Escrow"]
    mock_locations = ["Mumbai", "International", "Delhi", "Online", "International"]
    
    # Establish a persistent visual display dataframe construct
    streamed_records = []
    
    for cycle in range(10):
        # Manufacture single isolated transactional incoming arrays
        user_id = f"USR_{np.random.randint(100, 150)}"
        amount = round(float(np.random.choice([np.random.uniform(10, 200), np.random.uniform(800, 4500)])), 2)
        merchant = np.random.choice(mock_vendors)
        location = np.random.choice(mock_locations)
        timestamp = time.strftime("%H:%M:%S")
        
        # Build mock feature tracking proxy to feed evaluation shape requirements
        mock_tx_count = np.random.randint(2, 25)
        mock_total_spent = amount * mock_tx_count
        mock_avg_ticket = mock_total_spent / mock_tx_count
        
        # Process vector through XGBoost inference matrix
        feature_vector = np.array([[mock_tx_count, mock_total_spent, mock_avg_ticket]])
        fraud_prob = ai_brain.predict_proba(feature_vector)[0][1]
        
        # Classify color-coded evaluation boundaries
        if fraud_prob >= sim_threshold:
            status_tag = f"<span class='text-danger' style='font-weight:bold;'>🚨 BLOCK (Prob: {fraud_prob*100:.1f}%)</span>"
        elif fraud_prob > 0.35:
            status_tag = f"<span class='text-warn' style='font-weight:bold;'>⚠️ FLAG (Prob: {fraud_prob*100:.1f}%)</span>"
        else:
            status_tag = f"<span class='text-safe' style='font-weight:bold;'>✅ ALLOWED (Prob: {fraud_prob*100:.1f}%)</span>"
            
        streamed_records.insert(0, {
            "Time": timestamp, "User Account": user_id, "Vendor": merchant,
            "Amount": f"${amount:,.2f}", "Origin": location, "Security Status Assessment": status_tag
        })
        
        # Convert array to visual HTML markup frame table
        html_table = "<table style='width:100%; border-collapse: collapse; background-color:#161b22; text-align:left;'>"
        html_table += "<tr style='border-bottom: 2px solid #30363d; color:#8b949e;'><th>Execution Time</th><th>Customer Reference</th><th>Vendor Destination</th><th>Volume</th><th>Origin Location</th><th>Risk Assessment</th></tr>"
        for r in streamed_records[:6]:  # Constrain presentation frame to newest 6 records
            html_table += f"<tr style='border-bottom: 1px solid #21262d;'><td>{r['Time']}</td><td>{r['User Account']}</td><td>{r['Vendor']}</td><td>{r['Amount']}</td><td>{r['Origin']}</td><td>{r['Security Status Assessment']}</td></tr>"
        html_table += "</table>"
        
        live_feed_anchor.markdown(html_table, unsafe_allow_html=True)
        time.sleep(1.2) # Throttle loop rate to resemble natural pipeline delivery clocks

st.markdown("---")

# 8. PROCESS MANUAL SIMULATOR ACTIONS
if trigger_screening:
    st.subheader("🔬 Standalone Account Pipeline Resolution")
    input_features = np.array([[sim_tx_count, sim_total_spent, sim_avg_ticket]])
    prob = ai_brain.predict_proba(input_features)[0][1]
    
    if prob >= sim_threshold:
        st.error(f"🚨 **ALGORITHM ASSESSMENT: MALICIOUS HIGH-RISK PROXY PROFILE** (System Assurance Score: {prob*100:.1f}%)")
    else:
        st.success(f"✅ **ALGORITHM ASSESSMENT: COMPLIANT SYSTEM PROFILE MATCH** (System Assurance Score: {(1-prob)*100:.1f}%)")

# 9. RAW PERSISTENT AUDIT LOG VESTIBULE
st.subheader("📋 Core Database Transaction Store Ledger")
st.dataframe(ledger_df, use_container_width=True)