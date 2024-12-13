"""API"""
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation de l'application FastAPI
app = FastAPI()

# Récupérer la clé API de Google à partir des variables d'environnement
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Créer une instance de ChatGoogleGenerativeAI pour interagir avec le modèle Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

class UserInput(BaseModel):
    """
    Modèle représentant les entrées de l'utilisateur.
    """
    question: str  # Le thème ou la question que l'utilisateur soumet
    temperature: float  # Température pour ajuster la créativité du modèle
    language: str  # Langue dans laquelle la réponse sera générée
    genre: str  # Genre de l'histoire (ex: aventure, fantasy, etc.)

# Route GET pour la racine (message de bienvenue)
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Fast-Accurate REPLY (FastA REPLY)!"}

# Route POST pour répondre à la question de l'utilisateur
@app.post("/answer")
def answer(user_input: UserInput):
    """
    Génère une réponse sous forme d'histoire en fonction de la question, de la température et de la langue fournie par l'utilisateur.
    Retourne une histoire générée par un modèle de langage via LangChain (Google Gemini).
    """
    # Créer un prompt structuré avec la question de l'utilisateur et le genre
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that generates creative stories."),
        ("user", f"Write a short story in {user_input.language} about {user_input.question} with a {user_input.genre} theme.")
    ])

    # Format du message pour l'API LangChain
    formatted_prompt = prompt.format_messages(question=user_input.question)

    # Interroger Google Gemini via LangChain pour obtenir une réponse
    #response = google_gemini.invoke(messages=formatted_prompt)
    ai_msg = llm.invoke(formatted_prompt)

     # Vérification si ai_msg contient l'attribut 'content'
    if hasattr(ai_msg, 'content'):
        return {
            "message": ai_msg.content  # réponse générée par Google Gemini
        }
    else:
        # Gérer les erreurs si la réponse ne contient pas 'content'
        return {
            "message": "Erreur : la réponse générée ne contient pas de texte valide."
        }
    
