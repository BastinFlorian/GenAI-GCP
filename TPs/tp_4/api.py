"FAST API"
from typing import List
from langchain_google_vertexai import VertexAIEmbeddings
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ingest import (
    create_cloud_sql_database_connection,
    get_embeddings,
    get_vector_store,
)
from retrieve import get_relevant_documents, format_relevant_documents
from config import TABLE_NAME


load_dotenv(dotenv_path=".env.template")

app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()


class UserInput(BaseModel):
    """
    Represents the user's input for querying relevant documents and generating an answer.

    Attributes:
    - question (str): The question or query text provided by the user.
    - temperature (float): The temperature setting for controlling the creativity of the language model's response.
    - language (str): The language in which the user wants the answer to be provided.
    """

    question: str
    temperature: float
    language: str


class DocumentResponse(BaseModel):
    """
    Represents the response format for a document, including its content and metadata.

    Attributes:
    - page_content (str): The main content of the document, such as text or relevant excerpts.
    - metadata (dict): Additional information about the document, such as its source or any tags.
    """

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
    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in relevant_docs
    ]


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

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_tokens=None,
        timeout=20,
        max_retries=2,
    )
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            (
                "system",
                f"You are a question answering chatbot. You must provide the answer in {user_input.language}.",
            ),
            (
                "human",
                f"The question is: {user_input.question}\n\nRelevant Information:\n{formatted_docs}",
            ),
        ]
    )

    chain = prompt | llm
    generate_answer = chain.invoke(
        {
            "language": user_input.language,
            "question": user_input.question,
        }
    ).content

    return {"message": generate_answer}
