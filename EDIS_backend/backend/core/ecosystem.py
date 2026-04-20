# backend/app/core/ecosystem.py

import numpy as np
from core.climate import get_climate_index_auto
from core.soilhealth import get_soil_index_auto
from core.vegetationstress import get_vegetation_index_auto
from core.humanpressure import get_human_pressure_index_auto
from core.biodiversity import get_biodiversity_index_auto

# ===============================
# DEFAULT WEIGHTS (must sum to 1)
# ===============================
DEFAULT_WEIGHTS = {
    "climate": 0.25,
    "soil": 0.25,
    "vegetation": 0.20,
    "human_pressure": 0.20,
    "biodiversity": 0.10
}

# ===============================
# HELPER FUNCTIONS
# ===============================

def normalize_weights(weights: dict):
    """
    Ensures weights sum to 1
    """
    total = sum(weights.values())
    if total == 0:
        return DEFAULT_WEIGHTS
    return {k: v / total for k, v in weights.items()}


def safe_extract(data: dict, key: str):
    """
    Extract value in 0–100 scale and convert to 0–1 safely
    """
    try:
        value = float(data.get(key, 0))
        return np.clip(value / 100.0, 0, 1)
    except (TypeError, ValueError):
        return 0.0


def classify_status(index_value: float):
    """
    Flexible classification logic
    """
    if index_value <= 0.33:
        return "Healthy"
    elif index_value <= 0.66:
        return "Moderate"
    else:
        return "High Risk / Near Collapse"


# ===============================
# MAIN COMPUTATION
# ===============================

def compute_ecosystem_index(lat, lon, weights=None):

    if weights is None:
        weights = DEFAULT_WEIGHTS

    weights = normalize_weights(weights)

    # Fetch values safely
    try:
        climate_data = get_climate_index_auto(lat, lon)
    except Exception:
        climate_data = {}

    try:
        soil_data = get_soil_index_auto(lat, lon)
    except Exception:
        soil_data = {}

    try:
        vegetation_data = get_vegetation_index_auto(lat, lon)
    except Exception:
        vegetation_data = {}

    try:
        human_data = get_human_pressure_index_auto(lat, lon)
    except Exception:
        human_data = {}

    try:
        biodiversity_data = get_biodiversity_index_auto(lat, lon)
    except Exception:
        biodiversity_data = {}

    # Convert to 0–1
    climate_val = safe_extract(climate_data, "climate_stress_0_100")
    soil_val = safe_extract(soil_data, "soil_stress_0_100")
    vegetation_val = safe_extract(vegetation_data, "vegetation_stress_0_100")
    human_val = safe_extract(human_data, "human_pressure_stress")
    biodiversity_val = safe_extract(biodiversity_data, "biodiversity_stress")

    # Weighted computation
    ecosystem_index = (
        weights["climate"] * climate_val +
        weights["soil"] * soil_val +
        weights["vegetation"] * vegetation_val +
        weights["human_pressure"] * human_val +
        weights["biodiversity"] * biodiversity_val
    )

    ecosystem_index = float(np.clip(ecosystem_index, 0, 1))
    resilience_index = 1 - ecosystem_index
    status = classify_status(ecosystem_index)

    return {
        "ecosystem_stress_index": round(ecosystem_index * 100, 2),
        "resilience_index": round(resilience_index * 100, 2),
        "status": status,
        "weights_used": weights,
        "components": {
            "climate": round(climate_val * 100, 2),
            "soil": round(soil_val * 100, 2),
            "vegetation": round(vegetation_val * 100, 2),
            "human_pressure": round(human_val * 100, 2),
            "biodiversity": round(biodiversity_val * 100, 2)
        }
    }
