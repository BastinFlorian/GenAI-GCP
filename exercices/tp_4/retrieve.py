import os
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_core.documents.base import Document
from config import TABLE_NAME


def get_relevant_documents(query: str, vector_store: PostgresVectorStore) -> list[Document]:
    """
    Retrieve relevant documents based on a query using a vector store.

    Args:
        query (str): The search query string.
        vector_store (PostgresVectorStore): An instance of PostgresVectorStore used to retrieve documents.

    Returns:
        list[Document]: A list of documents relevant to the query.
    """
    # Create the retriever using the vector store
    retriever = vector_store.as_retriever()
    
    # Perform the similarity search with the query
    return retriever.retrieve(query)


def format_relevant_documents(documents: list[Document]) -> str:
    """
    Format relevant documents into a string.

    Args:
        documents (list[Document]): A list of relevant documents.

    Returns:
        str: A string representation of the relevant documents.
    """
    return "\n".join([f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(documents)])


if __name__ == '__main__':
    # Test get_relevant_documents
    engine = create_cloud_sql_database_connection()
    embedding = get_embeddings()
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)
    
    # Retrieve relevant documents based on the query
    documents = get_relevant_documents("large language modelss", vector_store)
    assert len(documents) > 0, "No documents found for the query"

    # Test format_relevant_documents
    doc_str: str = format_relevant_documents(documents)
    assert len(doc_str) > 0, "No documents formatted successfully"

    print("All tests passed successfully.")
