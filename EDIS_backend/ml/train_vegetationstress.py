import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# ===============================
# 1️⃣ LOAD DATASET
# ===============================
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "vegetation_finalized.csv")
df = pd.read_csv(DATA_PATH)

FEATURES = ['ndvi_norm', 'vci_norm', 'tci_norm', 'vhi_norm']
TARGET = 'OVI'

X = df[FEATURES]
y = df[TARGET]

# ===============================
# 2️⃣ SPLIT DATA
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 3️⃣ TRAIN RANDOM FOREST
# ===============================
model = RandomForestRegressor(
    n_estimators=200,  # increased for better performance
    max_depth=10,      # optional: limit depth to prevent overfitting
    random_state=42
)

model.fit(X_train, y_train)

# ===============================
# 4️⃣ EVALUATE MODEL
# ===============================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")

# ===============================
# 5️⃣ SAVE MODEL
# ===============================

import os

# path to ml folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create saved_models folder
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

# save model
MODEL_PATH = os.path.join(MODEL_DIR, "vegetation_model.pkl")

joblib.dump(model, MODEL_PATH)

print("✅ Model saved at:", MODEL_PATH)