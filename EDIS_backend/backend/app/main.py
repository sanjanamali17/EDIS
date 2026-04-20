# backend/app/main.py
import numpy as np
from datetime import datetime
from fastapi import FastAPI, HTTPException
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import vegetationstress, soilhealth, humanpressure, climate, biodiversity

# Include router
from api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware


# =========================================================
# FASTAPI APP INITIALIZATION
# =========================================================
app = FastAPI(
    title="EDIS Backend",
    description="API for vegetation, soil, human pressure, climate, biodiversity, ecosystem analysis and EDIS chatbot",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router for POST endpoints
app.include_router(api_router, prefix="/api")

# =========================================================
# ROOT ENDPOINT
# =========================================================
@app.get("/")
def root():
    return {"message": "EDIS Backend Running. Use /docs for API documentation."}

# =========================================================
# HEALTH CHECK ENDPOINT
# =========================================================
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "EDIS Backend"
    }

#
#