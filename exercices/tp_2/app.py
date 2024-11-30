# api.py

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class UserInput(BaseModel):
    name: str
    genre: str
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
    greeting = f"Bonjour {'monsieur' if user_input.genre.lower() == 'male' else 'madame'} {user_input.name}"
    return {"message": greeting}

