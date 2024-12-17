# api.py
from fastapi import FastAPI
from pydantic import BaseModel

# Initialiser l'application FastAPI
app = FastAPI()

# Modèle pour valider les entrées utilisateur
class UserInput(BaseModel):
    name: str
    genre: str
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    # Générer un message basé sur les paramètres reçus
    if user_input.language == 'English' and user_input.genre.lower() == 'man':
        greeting = f"Hello Mr. {user_input.name}"
    elif user_input.language == 'English' and user_input.genre.lower() == 'woman':
        greeting = f"Hello Mrs. {user_input.name}"
    elif user_input.language == 'French' and user_input.genre.lower() == 'homme':
        greeting = f"Bonjour monsieur {user_input.name}"
    elif user_input.language == 'French' and user_input.genre.lower() == 'femme':
        greeting = f"Bonjour madame {user_input.name}"
    else:
        greeting = f"Hello {user_input.name}, your genre preference is {user_input.genre} and you speak {user_input.language}."

    return {"message": greeting}
