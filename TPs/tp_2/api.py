"""API"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        name (str): The name of the user.
        genre (str): The genre preference of the user.
        language (str): The language preference of the user.
    """

    name: str  # Nom de l'utilisateur
    genre: str  # Genre de l'utilisateur
    language: str  # Langue de l'utilisateur


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.

    Args:
        user_input (UserInput): An object containing user details such as name, genre, and language.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    # Génération d'un message de salutation
    return {
        "message": f"Hello {user_input.genre} {user_input.name}, you speak {user_input.language}!"
    }
