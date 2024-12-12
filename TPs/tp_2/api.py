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
    # TODO fill the required attributes


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.
    Args:
        user_input (UserInput): An object containing user details such as name, genre, and language.
    Returns:
        dict: A dictionary containing a greeting message.
    """
    # TODO edit the implementation to match the required ouput from #1
    return {"message": f"Hello Mr {user_input.name} from {user_input.genre}, {user_input.language}"}