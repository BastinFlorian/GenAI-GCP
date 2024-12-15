"""API"""
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        prompt (str): The prompt of the user.
        temperature (float): The temperature for AI response variability.
        language (str): The preferred language for the response.
    """

    prompt: str
    temperature: float
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a short story based on the user's theme.
    Args:
        user_input (UserInput): An object containing the user's details.
    Returns:
        dict: A dictionary containing the generated short story.
    """
    # Initialize the AI model with user-defined temperature
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Define the prompt template with placeholders
    template = ChatPromptTemplate(
        [
            (
                "system",
                "You are a helpful AI bot that generates a short story."
                "Your name is {name}."
                "You answer in {language}. You don't introduce yourself."
                "You don't introduce your stories. "
                "You start directly with your storytelling."
            ),
            ("human", "Hello, how are you doing?"),
            ("ai", "I'm good, thanks! Which theme would interest you?"),
            ("human", "The theme of the short story is {prompt}"),
        ]
    )

    # Invoke the template with user input values
    prompt_value = template.invoke(
        {
            "name": "ThemeChat",
            "language": user_input.language,
            "prompt": user_input.prompt,
        }
    )

    # Generate AI response
    ai_msg = llm.invoke(prompt_value)

    return {"message": ai_msg.content}
