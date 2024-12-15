"""API"""

# Backend de l'application utilisant FastAPI.
# Reçoit des données utilisateur via une requête POST et génère un message de salutation personnalisé.


from fastapi import FastAPI
from pydantic import BaseModel

# Initialiser l'application FastAPI
app = FastAPI()

# Modèle de données pour valider les entrées utilisateur
class UserInput(BaseModel):
    """
    Modèle pour les données utilisateur.
    Attributs :
        - name (str) : Nom de l'utilisateur.
        - genre (str) : Genre sélectionné (Homme/Femme ou Man/Woman).
        - language (str) : Langue sélectionnée (English/French).
    """
    name: str
    genre: str
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    """
    Point de terminaison pour générer un message de salutation.
    
    Args:
        user_input (UserInput): Données utilisateur.

    Returns:
        dict: Message de salutation basé sur les préférences utilisateur.
    """
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
