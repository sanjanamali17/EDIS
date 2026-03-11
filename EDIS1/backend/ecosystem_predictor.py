"""
Future Ecosystem Predictor Module
Earth Digital Immune System (EDIS)

This module provides AI-powered ecosystem health predictions
using historical environmental indicators and machine learning.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple, Optional

class EcosystemPredictor:
    """
    AI-powered ecosystem health prediction engine
    """
    
    def __init__(self):
        self.models = {}  # Store trained models for each city
        self.historical_data = {}  # Store processed historical data
        self.esi_weights = {
            'climate_stress': 0.25,
            'soil_stress': 0.20,
            'vegetation_stress': 0.20,
            'human_pressure': 0.20,
            'biodiversity_stress': 0.15
        }
        
    def calculate_esi(self, row: pd.Series) -> float:
        """
        Calculate Ecosystem Stress Index (ESI) using weighted environmental indicators
        
        Formula:
        ESI = 0.25 * climate_stress + 0.20 * soil_stress + 0.20 * vegetation_stress + 
              0.20 * human_pressure + 0.15 * biodiversity_stress
        
        Args:
            row: Pandas Series containing environmental indicators
            
        Returns:
            ESI value (0-100)
        """
        try:
            esi = (
                self.esi_weights['climate_stress'] * row['climate_stress'] +
                self.esi_weights['soil_stress'] * row['soil_stress'] +
                self.esi_weights['vegetation_stress'] * row['vegetation_stress'] +
                self.esi_weights['human_pressure'] * row['human_pressure'] +
                self.esi_weights['biodiversity_stress'] * row['biodiversity_stress']
            )
            return round(esi, 2)
        except Exception as e:
            print(f"Error calculating ESI: {e}")
            return 0.0
    
    def classify_ecosystem_status(self, esi: float) -> str:
        """
        Classify ecosystem status based on ESI value
        
        Args:
            esi: Ecosystem Stress Index value
            
        Returns:
            Ecosystem status string
        """
        if esi < 30:
            return "Healthy Ecosystem"
        elif esi < 60:
            return "Moderate Stress"
        else:
            return "High Ecosystem Risk"
    
    def load_historical_data(self, data_path: str) -> bool:
        """
        Load and process historical environmental data
        
        Args:
            data_path: Path to the CSV file containing historical data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load the historical data
            df = pd.read_csv(data_path)
            
            # Calculate ESI for each row
            df['esi'] = df.apply(self.calculate_esi, axis=1)
            df['ecosystem_status'] = df['esi'].apply(self.classify_ecosystem_status)
            
            # Group data by city
            self.historical_data = {}
            for city in df['name'].unique():
                city_data = df[df['name'] == city].sort_values('year')
                self.historical_data[city] = city_data
                
            print(f"Loaded historical data for {len(self.historical_data)} cities")
            return True
            
        except Exception as e:
            print(f"Error loading historical data: {e}")
            return False
    
    def train_city_model(self, city: str) -> bool:
        """
        Train Linear Regression model for a specific city
        
        Args:
            city: City name to train model for
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if city not in self.historical_data:
                print(f"No historical data available for {city}")
                return False
            
            city_data = self.historical_data[city]
            
            # Check if we have enough data points
            if len(city_data) < 2:
                print(f"Insufficient data for {city}. Need at least 2 years of data.")
                return False
            
            # Prepare training data
            X = city_data[['year']].values.reshape(-1, 1)
            y = city_data['esi'].values
            
            # Train Linear Regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Calculate model performance
            y_pred = model.predict(X)
            mse = mean_squared_error(y, y_pred)
            r2 = r2_score(y, y_pred)
            
            # Store the model and metadata
            self.models[city] = {
                'model': model,
                'mse': mse,
                'r2_score': r2,
                'training_years': city_data['year'].tolist(),
                'training_esi': city_data['esi'].tolist(),
                'last_year': city_data['year'].max()
            }
            
            print(f"Model trained for {city} - R²: {r2:.3f}, MSE: {mse:.3f}")
            return True
            
        except Exception as e:
            print(f"Error training model for {city}: {e}")
            return False
    
    def predict_future_ecosystem(self, city: str, years_ahead: int) -> Dict:
        """
        Predict future ecosystem health for a city
        
        Args:
            city: City name to predict for
            years_ahead: Number of years to predict ahead
            
        Returns:
            Dictionary containing predictions and metadata
        """
        try:
            # Check if model exists for the city
            if city not in self.models:
                # Try to train the model
                if not self.train_city_model(city):
                    return {
                        'success': False,
                        'error': f'No model available for {city} and insufficient data to train'
                    }
            
            model_data = self.models[city]
            model = model_data['model']
            last_year = model_data['last_year']
            
            # Generate future years
            future_years = []
            for i in range(1, years_ahead + 1):
                future_years.append(last_year + i)
            
            # Make predictions
            future_years_array = np.array(future_years).reshape(-1, 1)
            predicted_esi = model.predict(future_years_array)
            
            # Prepare results
            predictions = []
            for i, year in enumerate(future_years):
                esi_value = round(predicted_esi[i], 2)
                status = self.classify_ecosystem_status(esi_value)
                
                predictions.append({
                    'year': year,
                    'esi': esi_value,
                    'status': status
                })
            
            # Calculate trend information
            trend_slope = model.coef_[0]
            trend_direction = "improving" if trend_slope < 0 else "declining"
            
            return {
                'success': True,
                'city': city,
                'predictions': predictions,
                'model_performance': {
                    'r2_score': round(model_data['r2_score'], 3),
                    'mse': round(model_data['mse'], 3)
                },
                'trend_analysis': {
                    'direction': trend_direction,
                    'slope': round(trend_slope, 3)
                },
                'training_data': {
                    'years': model_data['training_years'],
                    'esi_values': model_data['training_esi']
                }
            }
            
        except Exception as e:
            print(f"Error predicting future ecosystem for {city}: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Initialize the predictor
predictor = EcosystemPredictor()

# Load historical data on startup
def initialize_predictor():
    """Initialize the ecosystem predictor with historical data"""
    data_files = [
        'data/climate_instability_finalized.csv',
        'data/soil_degradation_finalized.csv',
        'data/vegetation_stress_finalized.csv',
        'data/human_pressure_finalized.csv',
        'data/biodiversity_loss_finalized.csv'
    ]
    
    # Try to load combined data or individual files
    combined_data_path = 'data/ecosystem_historical_data.csv'
    
    if os.path.exists(combined_data_path):
        predictor.load_historical_data(combined_data_path)
    else:
        # Load individual files and combine them
        try:
            # For now, we'll assume we have a combined file
            # In a real implementation, you'd merge the individual CSV files
            print("Combined historical data file not found. Please ensure data is available.")
        except Exception as e:
            print(f"Error initializing predictor: {e}")

if __name__ == "__main__":
    # Test the predictor
    initialize_predictor()
    
    # Example usage
    if predictor.historical_data:
        cities = list(predictor.historical_data.keys())[:3]  # Test with first 3 cities
        for city in cities:
            print(f"\nPredicting for {city}:")
            result = predictor.predict_future_ecosystem(city, 5)
            if result['success']:
                print(f"Predictions: {result['predictions']}")
                print(f"Trend: {result['trend_analysis']['direction']}")
            else:
                print(f"Error: {result['error']}")
