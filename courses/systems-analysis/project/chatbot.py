"""This module implements a chatbot using transformers for fine-tuning and RAG.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

import os
import numpy as np
import torch
import fitz
from datasets import Dataset, concatenate_datasets
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

class Chatbot:
    def __init__(self):
        self.model_name = "gpt2"
        self.model_save_path = "./results/model"
        self.concepts_path = "docs/concepts.pdf"
        self.updates_path = "docs/updates.pdf"
        self.max_length = 512
        
        # Initialize tokenizer
        self.tokenizer = self._setup_tokenizer()
        
        # Load or train model
        if os.path.exists(self.model_save_path):
            print("Loading trained model...")
            self.model = AutoModelForCausalLM.from_pretrained(self.model_save_path)
        else:
            print("Training new model...")
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self._train_model()

    def _setup_tokenizer(self):
        """Initialize and configure the tokenizer"""
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        with fitz.open(pdf_path) as doc:
            text = " ".join([page.get_text() for page in doc])
        return text

    def _prepare_dataset(self) -> Dataset:
        """Prepare training dataset from PDF files"""
        # Extract text from both PDFs
        concepts_text = self._extract_text_from_pdf(self.concepts_path)
        updates_text = self._extract_text_from_pdf(self.updates_path)
        
        # Create chunks of text
        def chunk_text(text, chunk_size=512):
            words = text.split()
            chunks = []
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i + chunk_size])
                chunks.append(chunk)
            return chunks

        # Create datasets from both texts
        concepts_chunks = chunk_text(concepts_text)
        updates_chunks = chunk_text(updates_text)
        
        # Combine both datasets
        dataset = Dataset.from_dict({
            "text": concepts_chunks + updates_chunks
        })
        
        return dataset

    def _tokenize_function(self, examples):
        """Tokenize text examples"""
        return self.tokenizer(
            examples["text"],
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_special_tokens_mask=True
        )

    def _train_model(self):
        """Fine-tune the model on our data"""
        # Prepare dataset
        dataset = self._prepare_dataset()
        tokenized_dataset = dataset.map(
            self._tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # We're not using masked language modeling
        )

        # Training arguments
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=5,             # Increase epochs
            per_device_train_batch_size=2,  # Reduce if memory issues
            learning_rate=2e-5,            # Slightly higher learning rate
            warmup_steps=200,              # More warmup steps
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            save_strategy="epoch",
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator
        )

        # Train model
        trainer.train()
        
        # Save model
        self.model.save_pretrained(self.model_save_path)
        self.tokenizer.save_pretrained(self.model_save_path)

    def generate_response(self, prompt: str) -> str:
        """Generate a response for the given prompt"""
        # Prepare input
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=self.max_length)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=self.max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # Decode and return response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(prompt, "").strip()