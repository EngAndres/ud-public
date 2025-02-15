"""This module is the entry point of the app.
Here the web services are just defined.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from chatbot import Chatbot

app = FastAPI()
chatbot = Chatbot()

# Data Models
class Query(BaseModel):
    """This class represents the data model for the query."""
    prompt: str

class Answer(BaseModel):
    """This class represents the data model for the answer."""
    prompt: str
    answer: str


@app.get("/", response_model=dict)
def read_root():
    """This is just a service to present the project in the root."""
    return {"Message": "Welcome to my chatbot project"}

@app.get("/healthcheck", response_model=dict)
def healthcheck():
    """This is just a service to validate API is running fine."""
    return {"Application": "MyChatbot", "Version": "0.0.1", "Status": "OK"}

@app.post("/chatbot/ask", response_model=Answer)
def ask_question(question: Query):
    """This is a service to ask a question to the chatbot.
    
    Args:
        question (str): The question to ask to the chatbot.
    
    Returns:
        The question and the answer from the chatbot.
    """
    try:
        answer = chatbot.generate_response(question.prompt)
        return Answer(prompt=question.prompt, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
