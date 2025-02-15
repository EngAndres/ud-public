"""This module has a class to train the chatbot.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

import os
import numpy as np
import torch
import faiss
from datasets import Dataset
import fitz
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)


class Chatbot:
    """This class represents the behavior of a chatbot using
    both fine-tunning and RAG to adjust it."""

    def __init__(self):
        self.fresh_data = ["docs/updates.pdf"]
        self.model_save_path = "./results/model"
        model_name = "distilbert-base-uncased"

        self.tokenizer = self._generate_tokenizer(model_name)
        
        if os.path.exists(self.model_save_path):
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_save_path
            )
        else:
            concepts_path = "docs/concepts.pdf"
            self.concepts = self._generate_dataset(concepts_path)
            self.model = self._load_foundational_model(model_name)
            self._fine_tunning()

        self.index = self._load_fresh_data(self.fresh_data)


    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def _embed(self, text: str) -> np.ndarray:
        """
        Computes a 768-dimensional embedding for the given text.

        Args:
            text (str): The text to embed.

        Returns:
            np.ndarray: The embedding vector.
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling on the token embeddings.
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.cpu().numpy()[0]

    def _load_foundational_model(
        self, model_name: str
    ) -> AutoModelForSequenceClassification:
        """This method loads the foundational model to fine-tune it.

        Args:
            model_name (str): The name of the model to load.

        Returns:
            The model.
        """
        # model_name = "distilbert-base-uncased"
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        return model

    def _generate_tokenizer(self, model_name: str) -> AutoTokenizer:
        """This method generates the tokenizer for the model.

        Args:
            model_name (str): The name of the model to load.

        Returns:
            The tokenizer.
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return tokenizer

    def _generate_dataset(self, path_concepts: str) -> Dataset:
        text_concepts = self._extract_text_from_pdf(path_concepts)
        dataset = Dataset.from_dict({"text": [text_concepts], "labels": [0]})
        return dataset

    def _tokenize_function(self, concepts: Dataset) -> dict:
        return self.tokenizer(concepts["text"], padding="max_length", truncation=True)

    def _fine_tunning(self):
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
        )

        tokenized_dataset = self.concepts.map(self._tokenize_function, batched=True)

        trainer = Trainer(
            model=self.model, args=training_args, train_dataset=tokenized_dataset
        )

        trainer.train()
        trainer.save_model(self.model_save_path)

    def _load_fresh_data(self, documents: list):
        index = faiss.IndexFlatL2(768)
        embeddings = np.vstack(
            [self._embed(self._extract_text_from_pdf(doc)) for doc in documents]
        ).astype(np.float32)
        index.add(embeddings)
        return index

    def _retrieve(self, query: str, documents: list):
        query_embedding = self._embed(query)
        _, i_ = self.index.search(np.array([query_embedding]), 1)
        return [documents[i] for i in i_[0]]

    def generate_response(self, prompt: str) -> str:
        """This method generates a response for a given prompt.

        Args:
            prompt (str): The prompt to generate the response.

        Returns:
            The response.
        """
        retrieved_document = self._retrieve(prompt, self.fresh_data)
        context = " ".join(retrieved_document)
        input_text = f"{context} {prompt}"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        output = self.model.generate(**inputs)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
