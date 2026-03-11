# backend/app/main.py
import numpy as np
from fastapi import FastAPI, HTTPException
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
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
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

#