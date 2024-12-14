"""API"""
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class UserInput(BaseModel):
    name: str
    genre: str
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
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