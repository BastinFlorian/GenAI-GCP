from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents
from config import TABLE_NAME
import logging

load_dotenv()

app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()

# Logger setup
logger = logging.getLogger(__name__)

class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

class UserInput(BaseModel):
    question: str
    temperature: float
    language: str
    documents: List[DocumentResponse]
    previous_context: List[dict]

@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    try:
        vector_store = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)
        relevants_docs = get_relevant_documents(
            f"Retrieve information related to: {user_input.question}", vector_store
        )
        if not relevants_docs:
            return []
        return [
            DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
            for doc in relevants_docs
        ]
    except Exception as e:
        logger.error(f"Error retrieving sources: {e}")
        return []

@app.post("/answer")
def answer(user_input: UserInput):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=user_input.temperature,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

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
                    1. Answer in {language} the QUESTION using the provided DOCUMENT text above.
                    2. Keep your answer grounded in the facts from the DOCUMENT whenever possible.
                    3. If the DOCUMENT does not contain enough information to fully answer the QUESTION, respond using your own knowledge. 
                    4. In your response, clearly indicate when the answer is based on your own knowledge and when it is based on the DOCUMENT.
                    5. Be concise but retain all relevant information, distinguishing between the sources of the answer.
                    6. If the question refers to "it" or any other ambiguous term, refer to the LAST DISCUSSED ENTITY unless further clarification is provided in the QUESTION.
                    7. Use the PREVIOUS CONTEXT only if it provides additional clarity or information that directly supports answering the QUESTION.

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
                "formatted_docs": format_relevant_documents(user_input.documents),
                "previous_context": user_input.previous_context,
                "last_entity": user_input.previous_context[-3:-1],
            }
        ).content
        return {"message": answer}
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return {"message": "An error occurred while generating the answer."}
