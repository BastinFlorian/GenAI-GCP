import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Charger les variables d'environnement
load_dotenv(dotenv_path=".env.template")

# Initialiser FastAPI
app = FastAPI()

# Charger la clé API Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    print(
        "Erreur : La clé API Google n'a pas été trouvée dans le fichier .env.template"
    )
else:
    print("La clé API a été chargée correctement")


# Modèle de données pour l'entrée utilisateur
class UserInput(BaseModel):
    question: str
    temperature: float
    language: str


# Route pour générer une histoire courte
@app.post("/generate_story")
def generate_story(user_input: UserInput):
    # Initialiser le modèle avec la clé API
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key=GOOGLE_API_KEY,
        temperature=user_input.temperature,
        max_tokens=500,
        max_retries=2,
    )

    # Template de prompt ajusté pour générer une histoire à partir d'un thème
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a masterful storyteller and literary artist with a boundless imagination. "
                "Your expertise lies in weaving immersive and evocative short stories in {language}. "
                "Transport the reader into a compelling narrative filled with rich imagery, intriguing characters, "
                "and unexpected twists, all inspired by the given theme.",
            ),
            (
                "human",
                "Here’s your challenge: Write a short story about the theme '{question}'. "
                "Craft a tale that surprises, delights, and resonates with the audience.",
            ),
        ]
    )

    # Formatage du prompt avec les valeurs dynamiques de l'utilisateur
    prompt_value = prompt_template.format(
        language=user_input.language,
        question=user_input.question,  # Ici, 'question' devient le thème
    )

    # Obtenir la réponse du modèle
    response = model.invoke(prompt_value)

    # Retourner la réponse sous format JSON
    return {
        "answer": response.content,  # Texte généré par le modèle
        "theme": user_input.question,  # Thème fourni par l'utilisateur
        "language": user_input.language,
        "temperature": user_input.temperature,
    }
