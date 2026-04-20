# backend/api/routes.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from typing import Dict, List, Optional
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
    ecosystem_score: Optional[float] = None
    indices: Optional[Dict[str, float]] = None
    messages: Optional[list] = None  # Add conversation history


class ChatResponse(BaseModel):
    reply: str
    intent: str
    visualize: Optional[str]


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
    error: Optional[str] = None

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

        memory.add_message(req.session_id, "user", req.message)
        memory.add_message(req.session_id, "assistant", result["text"])
        
        if req.messages and len(req.messages) > 0:
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

# FUTURE ECOSYSTEM PREDICTOR
# # =========================================================

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