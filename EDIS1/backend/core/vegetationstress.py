# backend/app/core/vegetationstress.py

from fastapi import HTTPException
import joblib
import pandas as pd
import numpy as np
import os
import hashlib

# ===============================
# PATHS
# ===============================
MODEL_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\ml\saved_models"
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\data\vegetation_finalized.csv"

MODEL_PATH = os.path.join(MODEL_DIR, "vegetation_ovi_model.pkl")

# ===============================
# LOAD MODEL (OPTIONAL)
# ===============================
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# ===============================
# LOAD DATASET
# ===============================
veg_df = pd.read_csv(DATA_PATH)
veg_df.columns = veg_df.columns.str.strip()

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
# NATIONAL BASE OVI
# ===============================
def get_latest_national_ovi():
    if "OVI" not in veg_df.columns:
        raise ValueError("Dataset missing 'OVI' column")

    df = veg_df

    if "year" in df.columns:
        latest_year = df["year"].max()
        row = df[df["year"] == latest_year].iloc[0]
    else:
        row = df.iloc[-1]

    vegetation_index = float(np.clip(row["OVI"], 0, 1))

    return vegetation_index

# ===============================
# DETERMINISTIC LOCATION VARIATION
# ===============================
def location_variation(lat, lon):
    key = f"{round(lat,3)}_{round(lon,3)}"
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)

    # Variation range: -0.15 to +0.15
    variation = ((hash_value % 31) - 15) / 100.0

    return variation

# ===============================
# AUTO MODE
# ===============================
def get_vegetation_index_auto(lat, lon):
    lat, lon = validate_location(lat, lon)

    base_ovi = get_latest_national_ovi()

    variation = location_variation(lat, lon)

    adjusted_ovi = base_ovi + variation

    adjusted_ovi = float(np.clip(adjusted_ovi, 0, 1))

    vegetation_stress = 1 - adjusted_ovi

    return {
        "vegetation_stress_0_100": round(vegetation_stress * 100, 2)
    }

# ===============================
# BACKWARD COMPATIBILITY
# ===============================
def get_vegetation_index(lat, lon):
    """
    Used by ecosystem.py
    Returns 0–1 vegetation index
    """
    lat, lon = validate_location(lat, lon)

    base_ovi = get_latest_national_ovi()
    variation = location_variation(lat, lon)

    adjusted_ovi = float(np.clip(base_ovi + variation, 0, 1))

    return adjusted_ovi
