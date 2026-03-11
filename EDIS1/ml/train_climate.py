"""
Climate Instability ML Pipeline
---------------------------------
Steps:
1. Load finalized dataset
2. Train Random Forest model and save
3. Define functions to fetch NASA POWER climate data
4. Compute features from NASA data
5. Make predictions using trained model
"""

import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# =========================
# Step 1: Load Dataset
# =========================
DATA_PATH = r'C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS\data\finalized\climate_instability_finalized.csv'
df = pd.read_csv(DATA_PATH)

print("Dataset Head:\n", df.head())
print("Dataset Info:\n")
print(df.info())

# =========================
# Step 2: Feature Selection
# =========================
X = df[['avg_mean_temp', 'rainfall', 'heatwave_frequency']]
y = df['climate_instability']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Step 3: Scaling
# =========================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# Step 4: Train Random Forest Model
# =========================
RF_model = RandomForestRegressor(n_estimators=200, random_state=42)
RF_model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = RF_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Climate Instability Model - MSE: {mse:.3f}, R²: {r2:.3f}")

# =========================
# Step 5: Save Model and Scaler
# =========================
MODEL_DIR = r"C:\Users\SANJANA MALI\OneDrive\Attachments\Desktop\EDIS1\ml\saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(RF_model, os.path.join(MODEL_DIR, "climate_model.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "climate_scaler.pkl"))

print("Model and scaler saved in:", MODEL_DIR)
# =========================
# Step 6: NASA POWER Fetch Function
# =========================
def fetch_nasa_power_climate(lat, lon, start_date="20230101", end_date="20231231"):
    """
    Fetch daily climate data from NASA POWER.
    Returns dictionary: 'T2M', 'T2M_MAX', 'PRECTOT' (or 'PRECTOTCORR')
    """
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"latitude={lat}&longitude={lon}"
        "&parameters=T2M,T2M_MAX,PRECTOT"
        f"&start={start_date}&end={end_date}"
        "&community=AG&format=JSON"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"NASA POWER API error: {response.status_code}")
    
    data = response.json()['properties']['parameter']
    
    # If PRECTOT missing, fallback to PRECTOTCORR
    if 'PRECTOT' not in data and 'PRECTOTCORR' in data:
        data['PRECTOT'] = data['PRECTOTCORR']
    
    return data

# =========================
# Step 7: Compute Features
# =========================
def compute_features_from_nasa(daily_data):
    """
    Convert NASA daily data into model features.
    Returns: avg_mean_temp, total_rainfall, heatwave_frequency
    """
    temp_avg = np.array(list(daily_data['T2M'].values()))
    temp_max = np.array(list(daily_data['T2M_MAX'].values()))
    
    # Rainfall
    if 'PRECTOT' in daily_data:
        rainfall = np.array(list(daily_data['PRECTOT'].values()))
    else:
        rainfall = np.zeros_like(temp_avg)
        print("Warning: precipitation missing, setting to 0.")
    
    avg_mean_temp = temp_avg.mean()
    total_rainfall = rainfall.sum()
    heatwave_frequency = np.sum(temp_max > 40)  # days with max temp > 40°C
    
    return avg_mean_temp, total_rainfall, heatwave_frequency

# =========================
# Step 8: Predict Climate Instability Index
# =========================
def get_climate_instability_index(lat, lon, start_date="20230101", end_date="20231231"):
    """
    Complete pipeline: NASA POWER -> features -> scaled input -> RF prediction
    Returns: Climate Instability Index (0-1 normalized)
    """
    # Fetch data
    daily_data = fetch_nasa_power_climate(lat, lon, start_date, end_date)
    
    # Compute features
    avg_temp, rainfall, heatwave_freq = compute_features_from_nasa(daily_data)
    
    # Load trained model & scaler
    model = joblib.load(os.path.join(MODEL_DIR, "climate_model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "climate_scaler.pkl"))
    
    # Prepare input
    X_input = np.array([[avg_temp, rainfall, heatwave_freq]])
    X_scaled = scaler.transform(X_input)
    
    # Predict
    climate_index = model.predict(X_scaled)[0]
    
    # Optional: normalize to 0-1 if needed
    climate_index = min(max(climate_index, 0), 1)
    
    return climate_index

# =========================
# Step 9: Example Usage
# =========================
if __name__ == "__main__":
    latitude = 28.6139   # New Delhi
    longitude = 77.2090
    
    climate_index = get_climate_instability_index(latitude, longitude)
    print(f"Climate Instability Index (New Delhi): {climate_index:.3f}")
    
    # Optional: fetch raw NASA POWER keys
    daily_data = fetch_nasa_power_climate(latitude, longitude)
    print("Available data keys:", daily_data.keys())
