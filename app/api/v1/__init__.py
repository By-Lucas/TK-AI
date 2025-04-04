from fastapi import APIRouter

from .endpoints import train_model
from .endpoints.analyzer import view_text_analysis


router = APIRouter()
router.include_router(train_model.router, tags=["Treinamento"])
router.include_router(view_text_analysis.router, prefix="/analyze", tags=["Análise"])
