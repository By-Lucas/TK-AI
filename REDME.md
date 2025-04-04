# 🧠 TK AI – Sistema de Análise de Sentimento com IA

Projeto desenvolvido para treinar uma Inteligência Artificial focada em **classificação de sentimento** de textos jornalísticos. A aplicação automatiza a coleta de dados, pré-processamento, treinamento e reuso do modelo utilizando tecnologias modernas de IA e arquitetura distribuída.

---

## 🚀 Tecnologias Utilizadas

- **FastAPI** – API web leve e performática
- **Transformers (Hugging Face)** – Treinamento de modelos NLP
- **PyTorch** – Backend de deep learning
- **Celery** – Execução assíncrona e agendamento de tarefas
- **RabbitMQ** – Broker de mensagens
- **Docker + Docker Compose** – Ambiente padronizado e replicável
- **Pandas / Datasets** – Manipulação de dados
- **PostgreSQL** (opcional) – Armazenamento de dados para extensões futuras

---

## 🧱 Estrutura do Projeto

```
tk_ai/
│
├── app/                          # App principal da API
│   ├── api/                      # Rotas (v1, v2...) organizadas por módulos
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── text_analysis.py
│   │       │   └── health_check.py
│   │       └── __init__.py
│   │
│   ├── core/                     # Configurações principais (env, segurança, logs)
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── settings.py
│   │
│   ├── services/                 # Lógica de negócio (NLP, Sentimento, Highlights)
│   │   ├── analyzer.py
│   │   ├── highlighter.py
│   │   └── sentiment.py
│   │
│   ├── models/                   # Modelos Pydantic (entrada e saída)
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   ├── utils/                    # Utilitários (helpers, normalizadores, etc.)
│   │   └── text_cleaner.py
│   │
│   └── main.py                   # Ponto de entrada do FastAPI
│
├── tests/                        # Testes automatizados (pytest)
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── scripts/                      # Scripts auxiliares (ex: treinamento, ingestão)
│   └── train_sentiment_model.py
│
├── .env                          # Variáveis de ambiente
├── Dockerfile                    # Dockerfile do app
├── docker-compose.yml            # Orquestração (banco, cache, etc.)
├── requirements.txt              # Dependências
├── pyproject.toml                # Config. opcional moderna (poetry ou setuptools)
├── README.md
└── .gitignore
```

## 2. Crie o .env com variáveis de ambiente
```
API_TOKEN=seu_token_jwt_aqui
ARTICLES_API_URL=https://sua-api.com/clipping/api/all-news/?company_id=1
```

## 3. Suba os serviços com Docker
```
docker-compose up --build
```

## 🔁 Fluxo Automatizado
- Coleta dados da API externa (notícias com texto e sentimento)
- Filtra e limpa os textos
- Evita duplicações com base nos IDs
- Salva em CSV
- Treina um modelo BERT com Hugging Face
- Salva o modelo com versionamento
- Pode ser reusado por pipelines de análise posterior

## 📡 Endpoints disponíveis
```
POST /v1/analyze/analyze
```
- **Payload:**
```
{
  "text": "A empresa teve resultados surpreendentes em 2024.",
  "highlight": "resultados"
}
```
- **Payload:**
```
{
  "highlight_found": true,
  "highlight_count": 1,
  "sentimento": "positivo"
}
```

## 📥 Treinar a IA manualmente
```
POST /v1/train/sentiment
```
**Payload:**
```
[
  {
    "texto": "A empresa está expandindo.",
    "sentimento": "positivo"
  },
  {
    "texto": "Resultados abaixo do esperado.",
    "sentimento": "negativo"
  }
]
```
