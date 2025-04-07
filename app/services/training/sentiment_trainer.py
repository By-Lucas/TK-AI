import os
import pandas as pd
from typing import Optional
from datetime import datetime

from datasets import Dataset
from transformers import (TrainerCallback, TrainerControl, 
                          TrainerState, TrainingArguments, AutoTokenizer, 
                          Trainer, AutoModelForSequenceClassification, 
                          EarlyStoppingCallback)



class PrintCallback(TrainerCallback):
    def on_epoch_begin(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        print(f"🚀 Iniciando época {state.epoch:.0f}")

    def on_epoch_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        print(f"✅ Finalizada época {state.epoch:.0f}")


class SentimentTrainer:
    def __init__(
        self,
        csv_path: str,
        model_name: str = "bert-base-multilingual-uncased",
        output_dir: str = "./traning/sentiment"
    ):
        self.csv_path = csv_path
        self.model_name = model_name
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def load_data(self) -> Dataset:
        df = pd.read_csv(self.csv_path)
        if "sentimento" not in df.columns:
            raise ValueError("O CSV precisa conter uma coluna chamada 'sentimento'.")

        self.labels = sorted(df["sentimento"].dropna().unique())
        self.label2id = {label: i for i, label in enumerate(self.labels)}
        self.id2label = {i: label for label, i in self.label2id.items()}

        if len(self.labels) < 2:
            raise ValueError("O dataset precisa conter pelo menos 2 classes diferentes para treinamento.")


        dataset = Dataset.from_pandas(df)

        # Tokenização
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        def tokenize(example):
            return tokenizer(example["texto"], padding="max_length", truncation=True)

        tokenized = dataset.map(tokenize, batched=True)

        # Codifica os rótulos
        def encode_labels(example):
            example["label"] = int(self.label2id[example["sentimento"]])
            return example

        tokenized = tokenized.map(encode_labels)
        tokenized.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

        self.tokenizer = tokenizer
        self.dataset = tokenized
        return tokenized

    def build_model(self):
        model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.labels),
            label2id=self.label2id,
            id2label=self.id2label
        )
        self.model = model
        return model

    def train(self, epochs: int = 3, batch_size: int = 8):
        log_dir = f"./logs/{self.timestamp}"
        model_dir = f"{self.output_dir}/{self.timestamp}"

        args = TrainingArguments(
            output_dir=model_dir,
            eval_strategy="epoch",  # ✅ Nome atualizado
            save_strategy="epoch",  # ✅ Alinhado
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=epochs,
            save_total_limit=2,
            logging_dir=log_dir,
            logging_steps=10,
            load_best_model_at_end=True
        )


        trainer = Trainer(
            model=self.model,
            args=args,
            train_dataset=self.dataset,
            eval_dataset=self.dataset,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
        )


        print(f"🔁 Iniciando treinamento com {len(self.dataset)} registros...")
        trainer.train()
        print(f"✅ Treinamento finalizado. Modelo salvo em: {model_dir}")

        return model_dir
