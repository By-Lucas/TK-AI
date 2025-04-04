from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

from app.tasks.train_sentiment_task import train_sentiment_model_task
from app.utils.cleaner import clean_text

router = APIRouter()

class TrainingItem(BaseModel):
    texto: str
    sentimento: str

@router.post("/train/sentiment")
def train_model(data: List[TrainingItem]):
    os.makedirs("data", exist_ok=True)

    registros = []
    for item in data:
        texto_limpo = clean_text(item.texto)
        sentimento = item.sentimento.lower().strip()

        # Validação de campos
        if not texto_limpo or not sentimento:
            continue  # Pula registros vazios

        registros.append({
            "texto": texto_limpo,
            "sentimento": sentimento
        })

    if not registros:
        return {"error": "Nenhum dado válido para treinamento."}

    df = pd.DataFrame(registros)
    df.to_csv("data/sentimentos.csv", index=False)

    train_sentiment_model_task.delay()

    return {"message": f"Treinamento iniciado via Celery com {len(df)} registros."}