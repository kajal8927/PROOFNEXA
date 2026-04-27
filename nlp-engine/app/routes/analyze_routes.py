from fastapi import APIRouter
from app.schemas.analyze_schema import AnalyzeRequest
from app.controllers.analyze_controller import analyze_text_controller

router = APIRouter()


@router.post("/analyze-text")
def analyze_text(payload: AnalyzeRequest):
    return analyze_text_controller(payload.text)
