from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import google.auth.exceptions
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()

# Initialisation de l'API Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Classes de validation pour les données d'entrée
class Query(BaseModel):
    question: str
    temperature: float
    language: str

class StoryRequest(BaseModel):
    theme: str
    temperature: float
    language: str

@app.post("/answer")
async def get_answer(query: Query):
    try:
        # Ajuster la température
        llm.temperature = query.temperature

        # Préparer les messages
        messages = [
            ("system", f"You are a helpful assistant that responds in {query.language}."),
            ("human", query.question),
        ]

        # Appeler Gemini et obtenir la réponse
        response = llm.invoke(messages)

        # Log de la réponse brute pour le débogage
        print("Response from Gemini:", response)

        # Vérification de la réponse avant d'extraire des informations
        if response and hasattr(response, 'content'):
            answer = response.content
        else:
            answer = "No valid response provided by the API."

        return JSONResponse(content={"answer": answer})

    except google.auth.exceptions.GoogleAuthError as e:
        print(f"Authentication error: {e}")
        raise HTTPException(status_code=403, detail="Authentication failed with Google API. Please check your credentials and API permissions.")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/generate_story")
async def generate_story(request: StoryRequest):
    try:
        # Ajuster la température
        llm.temperature = request.temperature

        # Préparer les messages pour générer une histoire
        messages = [
            ("system", f"You are a storyteller that generates stories in {request.language}."),
            ("human", f"Create a story based on the theme: {request.theme}."),
        ]

        # Appeler Gemini et obtenir la réponse
        response = llm.invoke(messages)

        # Log de la réponse brute pour le débogage
        print("Response from Gemini:", response)

        # Vérification de la réponse avant d'extraire des informations
        if response and hasattr(response, 'content'):
            story = response.content
        else:
            story = "No valid response provided by the API."

        return JSONResponse(content={"story": story})

    except google.auth.exceptions.GoogleAuthError as e:
        print(f"Authentication error: {e}")
        raise HTTPException(status_code=403, detail="Authentication failed with Google API. Please check your credentials and API permissions.")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
