from fastapi import APIRouter, HTTPException, Request
from app.schemas.analyze_schema import AnalyzeRequest, CompareTwoRequest, AnalyzeResponse
from app.controllers.analyze_controller import analyze_text_controller, compare_two_texts_controller
from app.config.config import settings
from app.config.database import get_db_status

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    """Checks NLP Service and Database status."""
    db_ok = get_db_status()
    if not db_ok:
        # We still return 200 or 503? Usually 503 if DB is down, but let's return a clear response.
        return {
            "status": "degraded",
            "database": "disconnected",
            "version": settings.VERSION
        }
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.VERSION
    }

@router.get("/version")
def get_version():
    """Returns the current version of the NLP engine."""
    return {"version": settings.VERSION}

@router.post("/analyze-text", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest):
    """Analyzes text against database submissions for plagiarism."""
    return analyze_text_controller(payload.text, payload.submissionId)

@router.post("/compare-two-texts", response_model=AnalyzeResponse)
def compare_two_texts(payload: CompareTwoRequest):
    """Compares two texts directly without database lookup."""
    return compare_two_texts_controller(payload.text1, payload.text2)
