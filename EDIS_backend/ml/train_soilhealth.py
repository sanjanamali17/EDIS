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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
DATA_PATH = os.path.join(DATA_DIR, "soilhealth_finalized.csv")

os.makedirs(SAVE_DIR, exist_ok=True)

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(DATA_PATH)

FEATURES = ["Moisture", "Nitrogen", "Phosphorous", "Potassium"]
TARGET = "SDI"

X = df[FEATURES]
y = df[TARGET]

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
joblib.dump(model, os.path.join(SAVE_DIR, "soil_model.pkl"))
joblib.dump(scaler, os.path.join(SAVE_DIR, "soil_scaler.pkl"))

print("✅ Soil SDI model and scaler saved.")
