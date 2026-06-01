import logging
import os
import subprocess
import sys
from pathlib import Path

# 1. Define Project Structural Root
ROOT_DIR = Path(__file__).resolve().parent
LOG_FILE_PATH = ROOT_DIR / "system_activity.log"

# 2. Configure Industry-Grade Dual-Target Logging Infrastructure
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),  # Save logs to a permanent audit file
        logging.StreamHandler(sys.stdout)                     # Simultaneously echo to developer terminal
    ]
)


def run_script(script_relative_path):
    """Executes an isolated pipeline script layer with absolute error monitoring"""
    script_absolute_path = ROOT_DIR / script_relative_path

    logging.info(f"🚀 Executing Pipeline Stage: {script_relative_path.name}")

    # Launch subprocess in exact environment context
    result = subprocess.run([sys.executable, str(script_absolute_path)])

    # Robust Exception Handling: Catch crashes before they disrupt core application stability
    if result.returncode != 0:
        logging.error(f"❌ CRITICAL PIPELINE BREAK: System failure in '{script_relative_path.name}' with return exit code {result.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    logging.info("=====================================================")
    logging.info("⚡ LAUNCHING PRODUCTION FINTECH DATA & AI CORE ⚡")
    logging.info("=====================================================")

    try:
        # --- PHASE 0: DATA TRANSFORMATION PIPELINE ---
        run_script(Path("src/pipeline/generate_synthetic_data.py"))
        run_script(Path("src/pipeline/clean_data.py"))
        run_script(Path("src/pipeline/ingest_data.py"))

        # --- PHASE 1: COMPLIANCE & RISK METRIC STORES ---
        run_script(Path("src/analytics/update_profiles.py"))
        run_script(Path("src/analytics/risk_scoring.py"))

        # --- PHASE 2: AUTOMATED AI CLASSIFICATION SYSTEM ---
        run_script(Path("src/models/train_model.py"))
        run_script(Path("src/models/predict_live.py"))

        logging.info("=====================================================")
        logging.info("🎉 SUCCESS: END-TO-END SYSTEM CYCLE COMPLETE 🎉")
        logging.info("=====================================================")

    except Exception as system_fault:
        logging.critical(f"🚨 UNHANDLED SYSTEM FAULT OVERRIDE: {str(system_fault)}")
        sys.exit(1)