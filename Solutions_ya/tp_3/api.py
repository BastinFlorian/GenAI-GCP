from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

# Vérifier si la clé API Google est définie
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("Google API Key is missing. Please set it in the .env file.")

app = FastAPI()

# Define the data model for user input
class UserQuestion(BaseModel):
    question: str
    temperature: float
    language: str

@app.post("/answer")
def answer(user_question: UserQuestion):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_question.temperature,
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
            "language": user_question.language,
            "input": user_question.question,
        })
    return {
        "message": ai_msg.content 
    }
