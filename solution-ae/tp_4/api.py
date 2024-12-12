import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_google_cloud_sql_pg import PostgresEngine
from typing import Optional
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents
from config import  TABLE_NAME

load_dotenv()

app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()

class UserInput(BaseModel):
    question: str
    temperature: float
    language: str

class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    """
    Endpoint to retrieve relevant documents based on a user's query.

    Args:
    - user_input (UserInput): The user input containing the question, temperature, and language.

    Returns:
    - List[DocumentResponse]: A list of documents relevant to the user's query, including content and metadata.
    """
    vector_store = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)
    relevant_docs = get_relevant_documents(user_input.question, vector_store)
    return [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in relevant_docs]

@app.post("/answer")
def answer(user_input: UserInput):
    """
    Endpoint to generate an answer based on a user's question and relevant documents.

    Args:
    - user_input (UserInput): The user input containing the question, temperature, and language.

    Returns:
    - dict: A dictionary containing the generated answer as a "message" field.
    """
    vector_store = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)  
    relevant_docs = get_relevant_documents(user_input.question, vector_store)
    formatted_docs = format_relevant_documents(relevant_docs)
    formatted_prompt = f"""
    You are a question-answering chatbot. Use the provided document, and entities to deliver precise and well-informed answers.
    Follow these instructions:
    1. Respond in {user_input.language} to the {user_input.question}, utilizing information from the {formatted_docs}.
    2. Base your answers on the {formatted_docs}, ensuring your responses are factual and grounded.
    3. If the {formatted_docs} lacks sufficient information, use your general knowledge to answer and clearly indicate when external information is used.
    4. Keep responses concise but comprehensive, including all essential details.
    5. The question is {user_input.question}.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    prompt_template = ChatPromptTemplate.from_template(formatted_prompt)
    chain = prompt_template | llm
    gen_answer = chain.invoke({
        "language": user_input.language,
        "question": user_input.question,
        "formatted_docs": formatted_docs,
    }).content
    return {"message": gen_answer}
