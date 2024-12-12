"""
API for generating responses using Google Gemini model via LangChain.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the API
app = FastAPI()


class UserInput(BaseModel):
    """
    Model for user input containing the question, temperature, and
    language preference.
    """
    question: str  # The theme for the story
    temperature: float  # Temperature for creativity
    language: str  # Language preference


# Configure the Google Gemini model via LangChain
chat_model = ChatGoogleGenerativeAI(
    api_key=GOOGLE_API_KEY, model="gemini-pro"
)

# Define a prompt template for generating responses
prompt_template = ChatPromptTemplate.from_template(
    "Write a short story based on the theme '{question}' in {language}. "
    "Use a creativity level of {temperature}."
)


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Endpoint to respond to user questions using a language model.
    """
    # Create the prompt using user input
    prompt = prompt_template.format(
        question=user_input.question,
        temperature=user_input.temperature,
        language=user_input.language
    )

    # Generate a response using the model
    try:
        response = chat_model.invoke(prompt)
        response_message = response.content
    except ValueError as e:
        response_message = f"Error generating response: {e}"
    except TypeError as e:
        response_message = f"Type error: {e}"

    # Return the formatted response
    return {"message": response_message}
