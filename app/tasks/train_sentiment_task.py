from app.tasks.celery_worker import celery
from app.services.training.sentiment_trainer import SentimentTrainer

@celery.task(bind=True, max_retries=3, default_retry_delay=60, name="train_sentiment_model_task")
def train_sentiment_model_task(self):
    try:
        trainer = SentimentTrainer(csv_path="data/sentimentos.csv")
        trainer.load_data()
        trainer.build_model()
        path = trainer.train()

        return f"✅ Modelo treinado com sucesso em: {path}"

    except Exception as e:
       return f"❌ Erro no treinamento: {str(e)}"
