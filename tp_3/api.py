"""API"""
from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (clé API de Google)
load_dotenv()

app = FastAPI()

# Définir le modèle de données d'entrée
class UserInput(BaseModel):
    question: str
    temperature: float
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    """
    Cette fonction génère une réponse basée sur la question de l'utilisateur, la température et la langue.
    """
    
    # Charger la clé API depuis l'environnement
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    # Initialiser le modèle Gemini avec LangChain
    generative_ai = ChatGoogleGenerativeAI(api_key=google_api_key)
    
    # Configurer le prompt pour la langue
    if user_input.language == "French":
        prompt = f"Répondez à la question suivante en français: {user_input.question}"
    elif user_input.language == "Arabic":
        prompt = f"أجب على السؤال التالي باللغة العربية: {user_input.question}"
    else:
        prompt = f"Answer the following question in English: {user_input.question}"
    
    # Générer la réponse avec le modèle
    answer = generative_ai.generate(prompt, temperature=user_input.temperature)
    
    # Retourner la réponse sous forme d'une phrase structurée
    return {
        "message": f"The user asked the question: '{user_input.question}' in {user_input.language} with a temperature of {user_input.temperature}. The answer is: {answer}"
    }
