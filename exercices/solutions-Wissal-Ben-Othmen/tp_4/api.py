"""
API module for question-answering application
using FastAPI and Google Generative AI.
"""

from typing import List
import dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ingest import get_embeddings
from retrieve import search_documents, initialize_vector_store

# Load environment variables
dotenv.load_dotenv()

app = FastAPI()

# Initialize once and reuse
EMBEDDING = get_embeddings()  # VertexAI Embeddings instance


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        question (str): The question of the user.
        temperature (float): The temperature for the LLM answer generation.
        language (str): The language preference of the user.
    """
    question: str
    temperature: float
    language: str


class DocumentResponse(BaseModel):
    """
    DocumentResponse is a data model representing a document response.

    Attributes:
        page_content (str): The content of the document.
        metadata (dict): Metadata associated with the document.
    """
    page_content: str
    metadata: dict


@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    """
    Perform a similarity search and
    return relevant documents based on the user input.

    Args:
        user_input (UserInput):
        The user input containing the query and preferences.

    Returns:
        List[DocumentResponse]: A list of relevant documents.
    """
    # Load the FAISS vector store
    vector_store = initialize_vector_store()

    # Perform similarity search using the question
    relevant_docs = search_documents(
        search_query=user_input.question,
        faiss_store=vector_store
    )

    # Format the response with content and metadata
    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in relevant_docs
    ]


@app.post("/answer")
def generate_answer(user_input: UserInput):
    """
    Generate an answer to a user's question using Google Generative AI.

    Args:
        user_input (UserInput):
        The user input containing the question and preferences.

    Returns:
        dict: A dictionary containing the generated answer.
    """
    # Initialize the LLM model from Google Generative AI
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Create a prompt for the LLM
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a question-answering assistant. "
            "You must provide your answers in {language}."
        ),
        ("human", "The question is: {question}"),
    ])

    # Format the prompt and send it to the LLM
    formatted_prompt = prompt.format(
        language=user_input.language,
        question=user_input.question
    )
    response = llm.invoke(formatted_prompt)

    return {"message": response.content}
# End-of-file (EOF)
