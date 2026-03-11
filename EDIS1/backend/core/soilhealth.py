# backend/app/core/soilhealth.py

import joblib
import numpy as np
import pandas as pd
import os
import hashlib
from fastapi import HTTPException

# ===============================
# PATHS
# ===============================
MODEL_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\ml\saved_models"
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\data\soilhealth_finalized.csv"

MODEL_PATH = os.path.join(MODEL_DIR, "soil_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "soil_scaler.pkl")

# ===============================
# LOAD MODEL & DATA
# ===============================
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load soil model/scaler: {e}")

soil_df = pd.read_csv(DATA_PATH)

FEATURE_COLUMNS = ["Moisture", "Nitrogen", "Phosphorous", "Potassium"]

# ===============================
# LOCATION VALIDATION
# ===============================
def validate_location(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    if not (6.0 <= lat <= 37.0 and 68.0 <= lon <= 98.0):
        raise HTTPException(status_code=400, detail="Only India supported")

    return lat, lon

# ===============================
# BASE NATIONAL FEATURES
# ===============================
def get_national_mean_features():
    return soil_df[FEATURE_COLUMNS].mean()

# ===============================
# DETERMINISTIC VARIATION
# ===============================
def location_variation(lat, lon):
    key = f"{round(lat,3)}_{round(lon,3)}"
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)

    # Variation multiplier range: -10% to +10%
    variation_factor = ((hash_value % 21) - 10) / 100.0

    return variation_factor

# ===============================
# AUTO MODE
# ===============================
def get_soil_index_auto(lat, lon):
    lat, lon = validate_location(lat, lon)

    base_features = get_national_mean_features()

    variation = location_variation(lat, lon)

    # Apply proportional variation to all soil nutrients
    varied_features = base_features * (1 + variation)

    features_df = pd.DataFrame([varied_features], columns=FEATURE_COLUMNS)

    features_scaled = scaler.transform(features_df)

    sdi = model.predict(features_scaled)[0]
    sdi = float(np.clip(sdi, 0, 1))

    return {
        "soil_stress_0_100": round(sdi * 100, 1)
    }
