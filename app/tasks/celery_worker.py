from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://tkuser:tkpass@rabbitmq:5672//")

celery = Celery("tk-ai", broker=CELERY_BROKER_URL)


# ⬇️ Importa as tasks para registrar no Celery
import app.tasks.train_sentiment_task
import app.tasks.celeryconfig
