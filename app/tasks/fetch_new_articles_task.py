import os
import requests
import pandas as pd


from app.tasks.celery_worker import celery
from app.services.training.sentiment_trainer import SentimentTrainer


API_URL = "https://news-qa.charismabi.space/clipping/api/all-news/?company_id=1"
API_TOKEN = os.getenv("API_TOKEN")  # Coloque seu token no .env
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}
PROCESSED_IDS_FILE = "data/ids_treinados.txt"

@celery.task(name="fetch_and_train_from_api_task")
def fetch_and_train_from_api_task():
    os.makedirs("data", exist_ok=True)
    resp = requests.get(API_URL, headers=HEADERS)

    if resp.status_code != 200:
        return f"❌ Erro ao acessar a API: {resp.status_code}"

    dados = resp.json().get("news", [])
    if not dados:
        return "✅ Nenhuma matéria encontrada."

    # Carrega IDs já treinados
    processados = set()
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE) as f:
            processados = set(f.read().splitlines())

    novos = []
    novos_ids = []

    for noticia in dados:
        id_noticia = str(noticia["id"])
        texto = noticia.get("text") or noticia.get("resume_text")
        sentimento = noticia.get("feeling") or noticia.get("tone")  # ou campo de rótulo real

        if not texto or not sentimento or id_noticia in processados:
            continue

        novos.append({
            "texto": texto.strip(),
            "sentimento": sentimento.lower().strip()
        })
        novos_ids.append(id_noticia)

    if not novos:
        return "✅ Nenhuma nova matéria válida para treinar."

    df = pd.DataFrame(novos)
    df.to_csv("data/sentimentos.csv", index=False)

    # Salva os novos IDs processados
    with open(PROCESSED_IDS_FILE, "a") as f:
        f.writelines([f"{nid}\n" for nid in novos_ids])

    # Treina IA
    trainer = SentimentTrainer(csv_path="data/sentimentos.csv")
    trainer.load_data()
    trainer.build_model()
    path = trainer.train()

    return f"✅ Treinamento finalizado com {len(df)} matérias. Modelo salvo em: {path}"
