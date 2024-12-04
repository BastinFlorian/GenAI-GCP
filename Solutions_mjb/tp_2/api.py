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
    #fill the required attributes
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
    # edit the implementation to match the required ouput from #1
    if user_input.language.lower() == "english":
        if user_input.genre.lower() == "man":
            return {"message": f"Hello Mr. {user_input.name}, welcome to the {user_input.genre} genre!"}
        elif user_input.genre.lower() == "woman":
            return {"message": f"Hello Ms. {user_input.name}, welcome to the {user_input.genre} genre!"}
    elif user_input.language.lower() == "french":
        if user_input.genre.lower() == "man":
            return {"message": f"Bonjour M. {user_input.name}, bienvenue dans le genre {user_input.genre}!"}
        elif user_input.genre.lower() == "woman":
            return {"message": f"Bonjour Mme {user_input.name}, bienvenue dans le genre {user_input.genre}!"}