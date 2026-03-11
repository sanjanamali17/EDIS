import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# ===============================
# 1️⃣ LOAD DATASET
# ===============================
DATA_PATH = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS1\data\vegetation_finalized.csv"
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
MODEL_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS1\ml\saved_models"
joblib.dump(model, f"{MODEL_DIR}/vegetation_ovi_model.pkl")

print("✅ Vegetation Random Forest model saved successfully.")
