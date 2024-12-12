from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
app = FastAPI()


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        prompt (str): The prompt of the user.
        temperature (float): The temperature of the ai.
        language (str): The language preference of the user.
    """
    
    question: str
    temperature: float
    language: str

@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generates a greeting message based on the user's input.
    Args:
        user_input (UserInput): An object containing user details such as name, genre, and language.
    Returns:
        dict: A dictionary containing a greeting message.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=None
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the best novelist in town. Your goal is to write a small original story constituted by a dozen of lines that could be a movie's synopsis in the theme proposed. The story has to be written in {language}.",
            ),
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm
    ai_msg = chain.invoke(
        {
            "language": user_input.language,
            "input": user_input.question,
        })
    return {
        "message": ai_msg.content 
    }