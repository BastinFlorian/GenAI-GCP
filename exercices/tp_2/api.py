from fastapi import FastAPI
from pydantic import BaseModel

# Define the request body model
class Question(BaseModel):
    name: str
    genre: str
    language: str

# Initialize FastAPI app
app = FastAPI()

# Define the POST endpoint
@app.post("/answer")
async def get_answer(question: Question):
    # Check the genre to provide a gender-specific response
    if question.genre == "female":
        greeting = "Bonjour madame"
    elif question.genre == "male":
        greeting = "Bonjour monsieur"
    else:
        greeting = "Hello"

    # Respond based on the name, genre, and language
    return {"message": f"{greeting} {question.name} from {question.genre}, {question.language}"}
