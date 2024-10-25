from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    name: str
    genre: str
    language: str

@app.post("/answer")
async def answer(data: UserInput):  # Make this function asynchronous
    return {"message": f"Hello {data.name}, you are {data.genre} and speak {data.language}!"}
