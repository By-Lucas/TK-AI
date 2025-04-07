import os
from app.tasks.celery_worker import celery
from app.services.training.sentiment_trainer import SentimentTrainer


@celery.task(bind=True, max_retries=3, default_retry_delay=60, name="train_sentiment_model_task")
def train_sentiment_model_task(self):
    try:
        # Verifica se o CSV existe
        if not os.path.exists("data/sentimentos.csv"):
            return "❌ Arquivo 'data/sentimentos.csv' não encontrado."

        # Treinamento direto a partir do CSV existente
        trainer = SentimentTrainer(csv_path="data/sentimentos.csv")
        trainer.load_data()
        trainer.build_model()
        path = trainer.train()

        return f"✅ Modelo treinado com sucesso! Salvo em: {path}"

    except Exception as e:
        raise self.retry(exc=e)
