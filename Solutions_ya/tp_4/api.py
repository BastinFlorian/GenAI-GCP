"""API"""
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ingest import create_cloud_sql_database_connection,get_embeddings,get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents
from config import TABLE_NAME

load_dotenv()
TABLE_NAME=os.environ["TABLE_NAME"]
app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict


class UserInput(BaseModel):
    """
    UserInput is a data model representing user input.

    Attributes:
        question (str): The question of the user.
        temperature (float): The temperature of the user.
        language (str): The language preference of the user.
        documents (List[DocumentResponse]): Retrieved documents for context.
    """

    question: str
    temperature: float
    language: str
    similarity_threshold: float
    documents: List[DocumentResponse]
    previous_context: List[dict]


@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    vector_store = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)
    relevants_docs = get_relevant_documents(
        f"Retrieve information related to: {user_input.question}", vector_store, user_input.similarity_threshold
    )

    if not relevants_docs:
        return []

    # else
    return [
        DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
        for doc in relevants_docs
    ]


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
        timeout=None,
        max_retries=2,
    )
    formatted_docs = format_relevant_documents(user_input.documents)
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            (
                "system",
                """DOCUMENT:
                {formatted_docs}

                PREVIOUS CONTEXT:
                {previous_context}

                LAST DISCUSSED ENTITY:
                {last_entity}

                INSTRUCTIONS:  
                    1. Respond in {language} to the {question}, using the information from the {document} provided.  
                    2. Ensure your response is directly grounded in the {document} whenever possible.  
                    3. If the {document} lacks sufficient information, use your general knowledge to answer, but clearly indicate when doing so.  
                    4. Keep your answer concise yet complete, including all relevant details and facts.  
                    5. Resolve ambiguous terms (e.g., "it") by referencing the {last_entity} unless the {question} specifies otherwise.  
                    6. Refer to the {previous_context} only if it directly clarifies or supplements the {question} or {document}.  

                QUESTION:
                {question}
                """,
            ),
            ("human", "The query is: {question}"),
        ]
    )

    chain = prompt | llm
    answer = chain.invoke(
        {
            "language": user_input.language,
            "question": user_input.question,
            "formatted_docs": formatted_docs,
            "previous_context": user_input.previous_context,
            "last_entity": user_input.previous_context[-3:-1],
        }
    ).content
    return {"message": answer,"formatted_docs" : formatted_docs}