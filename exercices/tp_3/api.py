from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Define the request model
class UserInput(BaseModel):
    question: str
    temperature: float
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generate a response based on user input.
    """
    response = (
        f"The user asked the question: '{user_input.question}' in '{user_input.language}' "
        f"with a temperature of '{user_input.temperature}'."
    )
    return {"message": response}
