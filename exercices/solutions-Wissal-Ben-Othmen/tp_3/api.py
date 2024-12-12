"""
This module defines a FastAPI application that
provides answers to user questions
using the Gemini model. It allows users
to specify the temperature and language
for the responses.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini model with Google API Key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", temperature=0.7
)

app = FastAPI()


class UserInput(BaseModel):
    """
    Represents the user input for the /answer endpoint.

    Attributes:
        question (str): The question asked by the user.
        temperature (float): The temperature for the model's response.
        language (str): The desired language for the response.
    """

    question: str
    temperature: float
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Answers a user's question using the Gemini model.

    Args:
        user_input (UserInput): The user's question, temperature, and language.

    Returns:
        dict: A dictionary containing the model's response.
    """
    # Update the model temperature with the user's input
    llm.temperature = user_input.temperature

    # Prepare the prompt based on language and question
    messages = [
        (
            "system",
            f"You are an assistant that answers in {user_input.language}.",
        ),
        ("human", user_input.question),
    ]

    # Invoke the model to generate a response
    ai_msg = llm.invoke(messages)

    return {"message": ai_msg.content}
# [missing-final-newline]
