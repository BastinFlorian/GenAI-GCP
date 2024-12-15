from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API Google
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Google API Key not found in the environment variables.")

# Initialiser FastAPI
app = FastAPI()

# Modèle de données pour la requête utilisateur
class UserInput(BaseModel):
    question: str  # Représente un thème pour la génération de l'histoire
    temperature: float = 0.5  # Valeur par défaut
    language: str = "English"  # Valeur par défaut

# Endpoint pour générer une histoire courte
@app.post("/generate-story")
def generate_story(user_input: UserInput):
    # Initialiser le modèle avec des paramètres avancés
    chat = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",  # Modèle puissant
        api_key=google_api_key,
        temperature=user_input.temperature,
        max_tokens=3000,
        max_retries=5,  # Réessayer plusieurs fois en cas d'erreur
    )

    # Construire les messages pour le modèle
    messages = [
        (
            "system",
            f"You are a highly creative and imaginative writer specializing in generating "
            f"short stories in {user_input.language}. Create an engaging and vivid short story "
            f"based on the following theme."
        ),
        ("human", user_input.question),
    ]

    try:
        # Envoyer une requête au modèle
        response = chat.invoke(messages)

        # Retourner l'histoire générée
        return {
            "story": response.content.strip(),
            "input_summary": {
                "question": user_input.question,
                "language": user_input.language,
                "temperature": user_input.temperature,
            },
        }
    except Exception as e:
        # Gestion des erreurs
        return {"error": f"An error occurred: {e}"}
