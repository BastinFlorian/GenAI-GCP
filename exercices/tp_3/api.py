"""API"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()
api_key = os.environ.get("GOOGLE_API_KEY")

class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        question (str): The user's question.
        temperature (float): The temperature parameter for the model.
        language (str): The language preference of the user.
    """
    question: str
    temperature: float
    language: str



@app.post("/answer")
def answer(user_input: UserInput):
    try:
        # Instancier le modèle Gemini
        gemini_model = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-1.5-pro",max_tokens=None,timeout=None,max_retries=2,  # Nom du modèle chat-bison
            temperature=user_input.temperature
        )

        # Créer un prompt
        # Ici, on reprend l'idée initiale : générer un message avec question et langue
        
        #chat = ChatPromptTemplate.from_messages([
           # ("system", "You are a helpful AI Assistant with a sense of humor"),
           # ("user", f"The user asked the question: {user_input.question} in {user_input.language}")
        #])
        chat = ChatPromptTemplate.from_messages([
            ("system", "You are a creative story-telling AI Assistant."),
            ("user", f"Write a short story in {user_input.language} about the theme '{user_input.question}'.")
        ])

        # Formater les messages pour le modèle
        prompt_messages = chat.format_messages()

        # Appel du modèle
        response = gemini_model.invoke(prompt_messages)

        return {"message": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
