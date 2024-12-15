from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents
from config import TABLE_NAME
#import logging

load_dotenv()

app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()

# Logger setup
#logger = logging.getLogger(__name__)

class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

class UserInput(BaseModel):
    question: str
    temperature: float
    language: str
    documents: List[DocumentResponse] = None

@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    vector_store = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)
    relevants_docs = get_relevant_documents(
        user_input.question,
        vector_store,
    )

    if not relevants_docs:
        return []

    # else
    return [
        DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
        for doc in relevants_docs ]


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Generate an answer based on the user's question and provided context.
    """
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=user_input.temperature,
        max_retries=2,
    )

    # Format documents for the prompt
    formatted_docs = (
        format_relevant_documents(user_input.documents)
        if user_input.documents else "No relevant documents provided."
    )

    # Prepare prompt template
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            (
                "system",
                """DOCUMENTS: {formatted_docs}
                
                INSTRUCTIONS:
                1. Answer in {language}.
                2. Use DOCUMENTS whenever possible to ground your response.
                3. If DOCUMENTS lack enough information, use general knowledge.
                4. Indicate the source of your response (DOCUMENTS or your knowledge).
                5. Be concise and prioritize relevant information.
                
                QUESTION:
                {question}""",
            ),
            ("human", "The query is: {question}"),
        ]
    )

    # Invoke the chain
    chain = prompt | llm
    response = chain.invoke({
        "language": user_input.language,
        "question": user_input.question,
        "formatted_docs": formatted_docs
    }).content
    
    return {"message": response}