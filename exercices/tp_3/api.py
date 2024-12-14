"""API"""
import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()


class UserInput(BaseModel):
    prompt: str
    temperature: float
    language: str


@app.post("/answer")
def answer(user_input: UserInput):
  
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    template = ChatPromptTemplate(
        [
            (
                "system",
                "You are a helpful AI bot that generates a short story based on the user's theme. Your name is {name}. You answer in {language}. You don't introduce yourself. You don't introduce your stories. You start directly your story-telling",
            ),
            ("human", "Hello, how are you doing?"),
            (
                "ai",
                "I'm doing well, thanks! What theme would you like for your short story?",
            ),
            ("human", "The theme of the short story is {user_input}"),
        ]
    )
    prompt_value = template.invoke(
        {
            "name": "Noveller the short story teller",
            "language": user_input.language,
            "user_input": user_input.prompt,
        }
    )
    ai_msg = llm.invoke(prompt_value)

    return {"message": ai_msg.content}
