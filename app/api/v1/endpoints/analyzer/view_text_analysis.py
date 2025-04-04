from fastapi import APIRouter

from app.schemas.analyzer.schema_analyzer import AnalyzeTextRequest, AnalyzeTextResponse
from app.services.analyzer.text_analyzer import analyze_text


router = APIRouter()

@router.post("/analyze", response_model=AnalyzeTextResponse)
def analyze(request: AnalyzeTextRequest):
    result = analyze_text(request.text, request.highlight)
    return AnalyzeTextResponse(**result)
