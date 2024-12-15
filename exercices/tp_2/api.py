from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class UserInput(BaseModel):
    name: str
    genre: str
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    message = f"Hello {user_input.name}! I see you like {user_input.genre} in {user_input.language}."
    return {"message": message}