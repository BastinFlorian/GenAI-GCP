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
    genre : str
    language : str


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.
    Args:
        user_input (UserInput): An object containing user details such as name, genre, and language.
    Returns:
        dict: A dictionary containing a greeting message.
    """

    if user_input.language == "English" and user_input.genre == "Man": 
        return {"message": f"Hello Mr {user_input.name} from {user_input.genre}, {user_input.language}"}
    elif user_input.language == "English" and user_input.genre == "Woman": 
        return {"message": f"Hello Mrs {user_input.name} from {user_input.genre}, {user_input.language}"}   
    elif user_input.language == "French" and user_input.genre == "Man" : 
        return {"message": f"Hello Mrs {user_input.name} from {user_input.genre}, {user_input.language}"}    
    else : 
        return {"message": f"Bonjour Mr {user_input.name} de {user_input.genre}, {user_input.language}"}
    

