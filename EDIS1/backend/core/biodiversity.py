from fastapi import HTTPException
import numpy as np
import pandas as pd
import os
import hashlib

# ===============================
# DATA PATH
# ===============================
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\FINAL_EDIS\EDIS1\data\biodiversity_dataset.csv"

biodiversity_df = pd.read_csv(DATA_PATH)

# ===============================
# UTILITIES
# ===============================
def to_0_100(value_0_1: float) -> int:
    return int(np.clip(value_0_1 * 100, 0, 100))

def biodiversity_health_to_stress(health_0_100: int) -> int:
    return int(np.clip(100 - health_0_100, 0, 100))

# ===============================
# GET NATIONAL BASE VALUE
# ===============================
def get_latest_national_stress():
    latest_year = biodiversity_df["year"].max()
    row = biodiversity_df[biodiversity_df["year"] == latest_year].iloc[0]

    raw_value = float(row["biodiversity_index"])

    health_0_100 = (
        to_0_100(raw_value) if raw_value <= 1 else int(raw_value)
    )

    return biodiversity_health_to_stress(health_0_100)

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

    # Create stable hash from coordinates
    key = f"{round(lat, 3)}_{round(lon, 3)}"
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)

    # Convert to range -15 to +15
    variation = (hash_value % 31) - 15

    return variation

# ===============================
# AUTO MODE
# ===============================
def get_biodiversity_index_auto(lat, lon):
    base_stress = get_latest_national_stress()

    variation = location_variation(lat, lon)

    final_score = base_stress + variation

    return {
        "biodiversity_stress": int(np.clip(final_score, 0, 100))
    }
