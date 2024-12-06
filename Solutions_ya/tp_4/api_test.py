from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents

load_dotenv()
TABLE_NAME = os.environ["TABLE_NAME"]
app = FastAPI()

# Initialize once and reuse
ENGINE = create_cloud_sql_database_connection()
EMBEDDING = get_embeddings()
VECTOR_STORE = get_vector_store(ENGINE, TABLE_NAME, EMBEDDING)

class UserInput(BaseModel):
    question: str
    temperature: float
    language: str
    similarity_threshold: float

class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    try:
        relevants_docs = get_relevant_documents(f"Retrieve information related to: {user_input.question}", VECTOR_STORE, user_input.similarity_threshold)
        if not relevants_docs:
            return []
        return [DocumentResponse(page_content=doc.page_content, metadata=doc.metadata) for doc in relevants_docs]
    except Exception as e:
        return {"error": str(e)}

@app.post("/answer")
async def answer(user_input: UserInput, background_tasks: BackgroundTasks):
    def generate_response():
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
                4. When your answer is based on your own knowledge, clearly indicate it in your response.
                5. Be somewhat concise but retain all relevant information and details.
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
        return chain.invoke({
            "language": user_input.language,
            "question": user_input.question,
            "formatted_docs": format_relevant_documents(user_input.documents)
        })

    background_tasks.add_task(generate_response)
    return {"status": "Processing"}
