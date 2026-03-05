from __future__ import annotations

from fastapi import FastAPI
from app.routers.patients import router as patients_router

app = FastAPI(
    title="Patient Management System API",
    version="1.0.0",
    summary="A small FastAPI project for managing patient records (JSON-backed).",
    contact={"name": "Research Team"},
)

@app.get("/", tags=["meta"])
def root():
    return {"message": "Patient Management System API", "docs": "/docs", "openapi": "/openapi.json"}

@app.get("/about", tags=["meta"])
def about():
    return {
        "message": "This API manages basic patient records stored in a JSON file. "
                   "For production, replace JSON storage with a real database."
    }

app.include_router(patients_router)
