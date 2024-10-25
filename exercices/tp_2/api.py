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

    name: str
    genre: str
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.
    Args:
        user_input (UserInput): An object containing user details such as name, genre, and language.
    Returns:
        dict: A dictionary containing a greeting message.
    """

    Args = {
        "English": [
            "Hello",
            {"Man": "Mr.", "Woman": "Ms.", "Homme": "Mr.", "Femme": "Ms."},
        ],
        "Français": [
            "Bonjour",
            {"Homme": "M.", "Femme": "Mme", "Man": "M.", "Woman": "Mme"},
        ],
    }

    return {
        "message": f"{Args[user_input.language][0]} {Args[user_input.language][1][user_input.genre]} {user_input.name}"
    }
