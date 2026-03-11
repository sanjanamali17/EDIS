# backend/api/routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import uuid

# Core ecosystem modules
from core import vegetationstress, soilhealth, humanpressure, climate, biodiversity
from core.ecosystem import compute_ecosystem_index

# Assistant modules
from edis_assistant.chat_engine import ask_edis_assistant
from edis_assistant.context_builder import build_context
from edis_assistant.memory import EDISMemory

# Services
from services.task_manager import submit_task, get_task_result
from services.report_generator import generate_pdf

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


class ChatResponse(BaseModel):
    reply: str
    intent: str
    visualize: str | None

# =========================================================
# METRIC ENDPOINTS (POST)
# =========================================================
@router.post("/analyze/vegetation")
def analyze_vegetation(data: LocationInput):
    try:
        result = vegetationstress.get_vegetation_index_auto(data.latitude, data.longitude)
        return {
            "vegetation_index": result.get("vegetation_index", 0),
            "vegetation_stress": result.get("vegetation_stress", 0),
            "vegetation_stress_0_100": result.get("vegetation_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/soil")
def analyze_soil(data: LocationInput):
    try:
        result = soilhealth.get_soil_index_auto(data.latitude, data.longitude)
        return {
            "soil_index": result.get("soil_index", 0),
            "soil_stress_0_100": result.get("soil_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/human-pressure")
def analyze_human_pressure(data: LocationInput):
    try:
        result = humanpressure.get_human_pressure_index_auto(data.latitude, data.longitude)
        return {
            "human_pressure_index": result.get("human_pressure_index", 0),
            "human_pressure_stress": result.get("human_pressure_stress", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/climate")
def analyze_climate(data: LocationInput):
    try:
        result = climate.get_climate_index_auto(data.latitude, data.longitude)
        return {
            "climate_index": result.get("climate_index", 0),
            "climate_stress_0_100": result.get("climate_stress_0_100", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/biodiversity")
def analyze_biodiversity(data: LocationInput):
    try:
        result = biodiversity.get_biodiversity_index_auto(data.latitude, data.longitude)
        return {
            "biodiversity_index": result.get("biodiversity_index", 0),
            "biodiversity_stress": result.get("biodiversity_stress", 0)
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

        return ChatResponse(
            reply=result["text"],
            intent=result["intent"],
            visualize=result.get("visualize")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# PDF REPORT
# =========================================================
@router.post("/analyze/ecosystem/report")
def download_report(data: LocationInput):
    try:
        analysis = compute_ecosystem_index(data.latitude, data.longitude)
        filename = f"/tmp/edis_report_{uuid.uuid4()}.pdf"
        generate_pdf(filename, analysis)
        return FileResponse(
            filename,
            media_type="application/pdf",
            filename="EDIS_Ecosystem_Report.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
