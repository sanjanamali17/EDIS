# backend/app/core/humanpressure.py

from fastapi import HTTPException
import joblib
import numpy as np
import pandas as pd
import os
import hashlib

# ===============================
# PATHS
# ===============================
MODEL_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\ml\saved_models"
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\data\humanpressure_finalized.csv"

MODEL_PATH = os.path.join(MODEL_DIR, "human_pressure_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "human_pressure_scaler.pkl")

# ===============================
# LOAD MODEL & DATA
# ===============================
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load human pressure model/scaler: {e}")

human_df = pd.read_csv(DATA_PATH)

# ===============================
# UTILITIES
# ===============================
def to_0_100(value_0_1: float) -> int:
    return int(np.clip(value_0_1 * 100, 0, 100))

# ===============================
# NATIONAL BASE VALUE
# ===============================
def get_latest_national_pressure():
    latest_year = human_df["year"].max()
    row = human_df[human_df["year"] == latest_year].iloc[0]

    raw_value = float(row["Human_Pressure"])

    value_0_100 = (
        to_0_100(raw_value) if raw_value <= 1 else int(raw_value)
    )

    return value_0_100

# ===============================
# DETERMINISTIC LOCATION VARIATION
# ===============================
def location_variation(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    if not (6.0 <= lat <= 37.0 and 68.0 <= lon <= 98.0):
        raise HTTPException(status_code=400, detail="Only India supported")

    key = f"{round(lat, 3)}_{round(lon, 3)}"
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)

    # Variation range: -20 to +20
    variation = (hash_value % 41) - 20

    return variation

# ===============================
# AUTO MODE
# ===============================
def get_human_pressure_index_auto(lat, lon):
    """
    Returns human pressure stress (0–100)
    """
    base_value = get_latest_national_pressure()

    variation = location_variation(lat, lon)

    final_score = base_value + variation

    return {
        "human_pressure_stress": int(np.clip(final_score, 0, 100))
    }
