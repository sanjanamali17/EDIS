import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# ===============================
# PATHS
# ===============================
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS1\data\humanpressure_finalized.csv"
SAVE_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS1\ml\saved_models"

os.makedirs(SAVE_DIR, exist_ok=True)

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(DATA_PATH)

X = df[
    [
        "groundwater_extraction_index_norm",
        "urban_expansion_percent_norm",
        "agricultural_intensity_index_norm",
        "population_density_change_percent_norm",
    ]
]

y = df["Human_Pressure"]

# ===============================
# SPLIT
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===============================
# MODEL
# ===============================
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# ===============================
# EVALUATION
# ===============================
y_pred = model.predict(X_test_scaled)
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"R² : {r2_score(y_test, y_pred):.4f}")

# ===============================
# SAVE
# ===============================
joblib.dump(model, os.path.join(SAVE_DIR, "human_pressure_model.pkl"))
joblib.dump(scaler, os.path.join(SAVE_DIR, "human_pressure_scaler.pkl"))

print("✅ Human Pressure model and scaler saved.")
