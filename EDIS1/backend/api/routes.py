# backend/api/routes.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import uuid
import os
import sys
import pandas as pd
import numpy as np
import json
import re

# Add the parent directory to the path to import the ecosystem predictor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ecosystem_predictor import EcosystemPredictor
from environmental_insights import EnvironmentalInsightGenerator

# ----------------------------
# Core ecosystem modules (dataset-driven)
# ----------------------------
from core import vegetationstress
from core import soilhealth
from core import humanpressure
from core import climate
from core import biodiversity

from core.ecosystem import compute_ecosystem_index

# ----------------------------
# Assistant modules
# ----------------------------
from edis_assistant.chat_engine import ask_edis_assistant
from edis_assistant.context_builder import build_context
from edis_assistant.memory import EDISMemory

# ----------------------------
# Services
# ----------------------------
from services.task_manager import submit_task, get_task_result
from services.report_generator import generate_pdf_bytes

router = APIRouter()
memory = EDISMemory()

# =========================================================
# MODELS
# =========================================================

class LocationInput(BaseModel):
    latitude: float
    longitude: float


class ChatRequest(BaseModel):
    session_id: str
    location: str
    message: str
    ecosystem_score: float | None = None
    indices: Dict[str, float] | None = None
    messages: list | None = None  # Add conversation history


class ChatResponse(BaseModel):
    reply: str
    intent: str
    visualize: str | None


class PredictionRequest(BaseModel):
    city: str
    years_ahead: int


class PredictionResponse(BaseModel):
    success: bool
    city: str
    predictions: List[Dict]
    model_performance: Dict
    trend_analysis: Dict
    training_data: Dict
    error: str = None

# =========================================================
# METRIC ENDPOINTS (DATASET-DRIVEN)
# =========================================================

@router.post("/analyze/climate")
def analyze_climate(data: LocationInput):
    try:
        result = climate.get_climate_index_auto(data.latitude, data.longitude)
        return {
            "climate_stress_0_100": result.get("climate_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/soil")
def analyze_soil(data: LocationInput):
    try:
        result = soilhealth.get_soil_index_auto(data.latitude, data.longitude)
        return {
            "soil_stress_0_100": result.get("soil_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/vegetation")
def analyze_vegetation(data: LocationInput):
    try:
        result = vegetationstress.get_vegetation_index_auto(data.latitude, data.longitude)
        return {
            
            "vegetation_stress_0_100": result.get("vegetation_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/biodiversity")
def analyze_biodiversity(data: LocationInput):
    try:
        result = biodiversity.get_biodiversity_index_auto(data.latitude, data.longitude)
        return {
            "biodiversity_stress": result.get("biodiversity_stress", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/human-pressure")
def analyze_human_pressure(data: LocationInput):
    try:
        result = humanpressure.get_human_pressure_index_auto(data.latitude, data.longitude)
        return {
            "human_pressure_stress": result.get("human_pressure_stress", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# ASYNC ECOSYSTEM ANALYSIS
# =========================================================

@router.post("/analyze/ecosystem/start")
def start_ecosystem_analysis(data: LocationInput):
    task_id = submit_task(compute_ecosystem_index, data.latitude, data.longitude)
    return {"task_id": task_id, "status": "started"}


@router.get("/analyze/ecosystem/status/{task_id}")
def ecosystem_analysis_status(task_id: str):
    result = get_task_result(task_id)
    if result["status"] == "completed":
        return {"status": "completed", "analysis": result["result"]}
    return result


# =========================================================
# EDIS ASSISTANT CHAT
# =========================================================

@router.post("/edis/chat", response_model=ChatResponse)
def chat_with_edis(req: ChatRequest):
    try:
        # Use frontend messages if provided, otherwise get from memory
        if req.messages:
            chat_history = req.messages
        else:
            chat_history = memory.get_chat(req.session_id)
        
        context = memory.get_last_context(req.session_id)

        if req.ecosystem_score is not None and req.indices:
            context = build_context(
                location=req.location,
                indices=req.indices,
                ecosystem_score=req.ecosystem_score
            )
            memory.save_context(req.session_id, context)

        result = ask_edis_assistant(
            user_query=req.message,
            context=context,
            chat_history=chat_history
        )

        # Save current messages to memory
        memory.add_message(req.session_id, "user", req.message)
        memory.add_message(req.session_id, "assistant", result["text"])
        
        # If frontend provided messages, sync them to memory
        if req.messages and len(req.messages) > 0:
            # Rebuild memory from frontend messages
            memory.clear_chat(req.session_id)
            for msg in req.messages:
                memory.add_message(req.session_id, msg["role"], msg["content"])

        return ChatResponse(
            reply=result["text"],
            intent=result["intent"],
            visualize=result.get("visualize")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# ECOSYSTEM HEALTH MAP API
# =========================================================

@router.get("/ecosystem-map-data")
def get_ecosystem_map_data():
    """
    Returns ecosystem data for all cities with coordinates for Geo-AI visualization
    """
    try:
        # City coordinates for major Indian cities
        city_coordinates = {
            "Delhi": {"lat": 28.6139, "lon": 77.2090},
            "Mumbai": {"lat": 19.0760, "lon": 72.8777},
            "Chennai": {"lat": 13.0827, "lon": 80.2707},
            "Bangalore": {"lat": 12.9716, "lon": 77.5946},
            "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
            "Jaipur": {"lat": 26.9124, "lon": 75.7873},
            "Kolkata": {"lat": 22.5726, "lon": 88.3639},
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
            "Pune": {"lat": 18.5204, "lon": 73.8567},
            "Kakinada": {"lat": 16.9437, "lon": 82.2350},
            "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
            "Vijayawada": {"lat": 16.5062, "lon": 80.6480},
            "Lucknow": {"lat": 26.8467, "lon": 80.9462},
            "Bhopal": {"lat": 23.2599, "lon": 77.4126},
            "Chandigarh": {"lat": 30.7333, "lon": 76.7794}
        }
        
        # Load ecosystem data from all datasets
        import pandas as pd
        
        # For now, use mock data based on the existing datasets
        # In production, this would load from actual CSV files
        mock_ecosystem_data = {
            "Delhi": {"climate_stress": 45.2, "soil_stress": 62.8, "vegetation_stress": 58.3, "human_pressure": 78.5, "biodiversity_stress": 52.1},
            "Mumbai": {"climate_stress": 38.7, "soil_stress": 54.2, "vegetation_stress": 41.6, "human_pressure": 71.3, "biodiversity_stress": 47.8},
            "Chennai": {"climate_stress": 42.1, "soil_stress": 48.9, "vegetation_stress": 45.7, "human_pressure": 65.2, "biodiversity_stress": 43.5},
            "Bangalore": {"climate_stress": 35.8, "soil_stress": 41.3, "vegetation_stress": 38.9, "human_pressure": 58.7, "biodiversity_stress": 39.2},
            "Hyderabad": {"climate_stress": 44.5, "soil_stress": 56.4, "vegetation_stress": 52.1, "human_pressure": 67.8, "biodiversity_stress": 48.6},
            "Jaipur": {"climate_stress": 52.3, "soil_stress": 68.7, "vegetation_stress": 61.2, "human_pressure": 54.3, "biodiversity_stress": 57.9},
            "Kolkata": {"climate_stress": 47.8, "soil_stress": 59.1, "vegetation_stress": 54.6, "human_pressure": 72.4, "biodiversity_stress": 51.3},
            "Ahmedabad": {"climate_stress": 49.6, "soil_stress": 63.5, "vegetation_stress": 57.8, "human_pressure": 61.2, "biodiversity_stress": 53.7},
            "Pune": {"climate_stress": 37.2, "soil_stress": 43.8, "vegetation_stress": 40.3, "human_pressure": 56.9, "biodiversity_stress": 41.5},
            "Kakinada": {"climate_stress": 28.4, "soil_stress": 62.5, "vegetation_stress": 77.0, "human_pressure": 64.0, "biodiversity_stress": 58.0},
            "Visakhapatnam": {"climate_stress": 33.7, "soil_stress": 51.2, "vegetation_stress": 46.8, "human_pressure": 59.3, "biodiversity_stress": 44.7},
            "Vijayawada": {"climate_stress": 36.9, "soil_stress": 54.7, "vegetation_stress": 49.2, "human_pressure": 57.8, "biodiversity_stress": 46.1},
            "Lucknow": {"climate_stress": 46.3, "soil_stress": 60.8, "vegetation_stress": 55.7, "human_pressure": 63.4, "biodiversity_stress": 50.9},
            "Bhopal": {"climate_stress": 41.5, "soil_stress": 52.3, "vegetation_stress": 47.6, "human_pressure": 58.1, "biodiversity_stress": 45.8},
            "Chandigarh": {"climate_stress": 39.8, "soil_stress": 46.7, "vegetation_stress": 43.1, "human_pressure": 55.6, "biodiversity_stress": 42.9}
        }
        
        # Get latest values for each city
        def get_latest_stress(data, city, stress_col):
            city_data = data[data['name'] == city]
            if len(city_data) > 0:
                # Get the most recent year's data
                latest = city_data.iloc[-1]
                if stress_col in latest:
                    return float(latest[stress_col])
            return 0.0
        
        ecosystem_data = []
        
        for city, coords in city_coordinates.items():
            # Get stress values from mock data
            city_data = mock_ecosystem_data.get(city, {
                "climate_stress": 30.0,
                "soil_stress": 40.0, 
                "vegetation_stress": 35.0,
                "human_pressure": 45.0,
                "biodiversity_stress": 38.0
            })
            
            climate_stress = city_data["climate_stress"]
            soil_stress = city_data["soil_stress"]
            vegetation_stress = city_data["vegetation_stress"]
            human_pressure = city_data["human_pressure"]
            biodiversity_stress = city_data["biodiversity_stress"]
            
            # Calculate Ecosystem Stress Index (weighted average)
            ecosystem_stress_index = (
                climate_stress * 0.25 +
                soil_stress * 0.25 +
                vegetation_stress * 0.2 +
                human_pressure * 0.2 +
                biodiversity_stress * 0.1
            )
            
            # Determine ecosystem status
            if ecosystem_stress_index < 30:
                ecosystem_status = "Healthy Ecosystem"
            elif ecosystem_stress_index < 60:
                ecosystem_status = "Moderate Stress"
            else:
                ecosystem_status = "High Ecosystem Stress"
            
            ecosystem_data.append({
                "city": city,
                "lat": coords["lat"],
                "lon": coords["lon"],
                "climate_stress": round(climate_stress, 2),
                "soil_stress": round(soil_stress, 2),
                "vegetation_stress": round(vegetation_stress, 2),
                "human_pressure": round(human_pressure, 2),
                "biodiversity_stress": round(biodiversity_stress, 2),
                "ecosystem_stress_index": round(ecosystem_stress_index, 2),
                "ecosystem_status": ecosystem_status
            })
        
        return {
            "success": True,
            "data": ecosystem_data,
            "total_cities": len(ecosystem_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading ecosystem map data: {str(e)}")


# =========================================================
# FUTURE ECOSYSTEM PREDICTOR
# =========================================================

# Initialize the ecosystem predictor
predictor = EcosystemPredictor()
insight_generator = EnvironmentalInsightGenerator()

@router.post("/predict-ecosystem", response_model=PredictionResponse)
def predict_future_ecosystem(request: PredictionRequest):
    """
    Predict future ecosystem health for a city using AI-powered time series analysis
    
    Args:
        request: PredictionRequest containing city and years_ahead
        
    Returns:
        PredictionResponse with future ecosystem predictions
    """
    try:
        # Initialize predictor with historical data if not already done
        if not predictor.historical_data:
            # Try to load historical data
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ecosystem_historical_data.csv")
            if not os.path.exists(data_path):
                # Create sample data for demonstration
                create_sample_historical_data()
            predictor.load_historical_data(data_path)
        
        # Make prediction
        result = predictor.predict_future_ecosystem(request.city, request.years_ahead)
        
        if result['success']:
            return PredictionResponse(**result)
        else:
            return PredictionResponse(
                success=False,
                city=request.city,
                predictions=[],
                model_performance={},
                trend_analysis={},
                training_data={},
                error=result.get('error', 'Unknown error occurred')
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting ecosystem: {str(e)}")


@router.post("/generate-insights")
def generate_environmental_insights(request: PredictionRequest):
    """
    Generate AI-powered environmental insights and recommendations based on ecosystem predictions
    
    Args:
        request: PredictionRequest containing city and years_ahead
        
    Returns:
        Dictionary containing insights, risks, and recommendations
    """
    try:
        # First get the prediction
        if not predictor.historical_data:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ecosystem_historical_data.csv")
            if not os.path.exists(data_path):
                create_sample_historical_data()
            predictor.load_historical_data(data_path)
        
        prediction_result = predictor.predict_future_ecosystem(request.city, request.years_ahead)
        
        if not prediction_result['success']:
            return {
                'success': False,
                'error': prediction_result.get('error', 'Failed to generate predictions')
            }
        
        # Generate insights
        insights = insight_generator.generate_insights(prediction_result)
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.get("/predictor/available-cities")
def get_available_cities():
    """
    Get list of cities available for prediction
    """
    try:
        if not predictor.historical_data:
            # Initialize predictor if not done
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ecosystem_historical_data.csv")
            if not os.path.exists(data_path):
                create_sample_historical_data()
            predictor.load_historical_data(data_path)
        
        cities = list(predictor.historical_data.keys())
        return {
            "success": True,
            "cities": cities,
            "total_cities": len(cities)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting available cities: {str(e)}")


def create_sample_historical_data():
    """
    Create sample historical data for demonstration purposes
    """
    try:
        import pandas as pd
        
        # Sample data for demonstration
        sample_data = []
        cities = ["Hyderabad", "Delhi", "Mumbai", "Bangalore", "Chennai"]
        years = [2018, 2019, 2020, 2021, 2022, 2023]
        
        for city in cities:
            for year in years:
                # Generate realistic-looking environmental indicators
                base_climate = 40 + (year - 2018) * 2 + np.random.normal(0, 3)
                base_soil = 35 + (year - 2018) * 1.5 + np.random.normal(0, 2)
                base_vegetation = 30 + (year - 2018) * 1.8 + np.random.normal(0, 2.5)
                base_human = 50 + (year - 2018) * 2.5 + np.random.normal(0, 4)
                base_biodiversity = 35 + (year - 2018) * 1.2 + np.random.normal(0, 3)
                
                sample_data.append({
                    'name': city,
                    'year': year,
                    'climate_stress': max(0, min(100, base_climate)),
                    'soil_stress': max(0, min(100, base_soil)),
                    'vegetation_stress': max(0, min(100, base_vegetation)),
                    'human_pressure': max(0, min(100, base_human)),
                    'biodiversity_stress': max(0, min(100, base_biodiversity))
                })
        
        # Create directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Save to CSV
        df = pd.DataFrame(sample_data)
        df.to_csv(os.path.join(data_dir, "ecosystem_historical_data.csv"), index=False)
        print(f"Created sample historical data with {len(sample_data)} records")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")


# =========================================================
# PDF REPORT
# =========================================================
from fastapi.responses import Response

@router.get("/download-report")
def download_report(lat: float, lon: float):

    try:
        result = compute_ecosystem_index(lat, lon)

        pdf_bytes = generate_pdf_bytes(result)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=ecosystem_report.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
