"""API"""
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        name (str): The name of the user.
        genre (str): The gender of the user, either "Man" or "Woman".
        language (str): The language preference of the user,
          either "English" or "French".
    """
    name: str
    genre: str
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.
    Args:
        user_input (UserInput): An object containing user
        details such as name, genre, and language.
    Returns:
        dict: A dictionary containing a greeting message.
    """
    # Determine greeting based on language and gender
    if user_input.language == "English" and user_input.genre == "Man":
        greeting = f"Hello Mr. {user_input.name}"
    elif user_input.language == "French" and user_input.genre == "Woman":
        greeting = f"Bonjour madame {user_input.name}"
    elif user_input.language == "English" and user_input.genre == "Woman":
        greeting = f"Hello Ms. {user_input.name}"
    elif user_input.language == "French" and user_input.genre == "Man":
        greeting = f"Bonjour monsieur {user_input.name}"
    else:
        greeting = f"Hello {user_input.name}"
    return {"message": greeting}
# [missing-final-newline]
