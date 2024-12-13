"""API"""
"""API"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Classe représentant l'input utilisateur
class UserInput(BaseModel):
    name: str  # Le nom de l'utilisateur
    genre: str  # Le genre de l'utilisateur
    language: str  # La langue de l'utilisateur

# Route GET pour la racine
@app.get("/")
def read_root():
    """
    Retourne un message de bienvenue à l'utilisateur.
    """
    return {"message": "Bienvenue sur l'API."}

# Route POST pour générer un message de salutation
@app.post("/answer")
def answer(user_input: UserInput):
    """
    Génère un message de salutation basé sur les informations de l'utilisateur.
    
    Args:
        user_input (UserInput): Un objet contenant le nom, le genre et la langue de l'utilisateur.

    Returns:
        dict: Un dictionnaire contenant le message de salutation.
    """
    # Logique de réponse en fonction de la langue et du genre
    if user_input.language == "Français":
        if user_input.genre == "Homme":
            message = f"Bonjour Monsieur {user_input.name}"
        elif user_input.genre == "Femme":
            message = f"Bonjour Madame {user_input.name}"
        else:
            message = f"Bonjour {user_input.name}"
    else:  # Default to English
        if user_input.genre == "Man":
            message = f"Hello Mr. {user_input.name}"
        elif user_input.genre == "Woman":
            message = f"Hello Ms. {user_input.name}"
        else:
            message = f"Hello {user_input.name}"
    
    return {"message": message}
