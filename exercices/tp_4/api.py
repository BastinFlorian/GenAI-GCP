"""
FastAPI application for question answering with document retrieval.

This module initializes embeddings, retrieves documents, and generates answers
using Google Generative AI.
"""

from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from ingest import get_embeddings
from retrieve import get_relevant_documents, load_vector_store

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize once and reuse
EMBEDDING = get_embeddings()  # VertexAI Embeddings instance


class UserInput(BaseModel):
    """UserInput model for question answering requests."""
    question: str
    temperature: float
    language: str


class DocumentResponse(BaseModel):
    """Document response model for search results."""
    page_content: str
    metadata: Dict


@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    """Get relevant documents based on user query."""
    try:
        vector_store = load_vector_store()
        relevant_docs = get_relevant_documents(
            search_query=user_input.question,
            inner_vector_store=vector_store
        )
        return [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in relevant_docs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving documents: {str(e)}"
        ) from e


@app.post("/answer")
def generate_answer(user_input: UserInput) -> Dict[str, str]:
    """Generate an answer using Google Generative AI."""
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=user_input.temperature,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Assistant: Answer questions in {language}."),
            ("human", "The question is: {question}"),
        ])
        chain = prompt.pipe(llm)
        response = chain.invoke({
            "language": user_input.language,
            "question": user_input.question,
        })
        return {"message": response.content}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating answer: {str(e)}"
        ) from e
