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
    retriever =  # TODO
    return retriever.invoke(query)

def format_relevant_documents(documents: list[Document]) -> str:
    """
    Format relevant documents into a str.

    Args:
        documents (list[Document]): A list of relevant documents.

    Returns:
        list[dict]: A list of dictionaries containing the relevant documents.

    Example:
        >>> documents = [
            Document(page_content: "First doc", metadata: {"title": "Doc 1"}),
            Document(page_content: "Second doc", metadata: {"title": "Doc 1"}
        ]s
        >>> doc_str: str = format_relevant_documents(documents)
        >>> '''
            Source 1: First doc
            -----
            Source 2: Second doc
        '''
    """
    # TOUPDATE with example in docstring
    return "\n".join([doc.page_content for doc in documents])


if __name__ == '__main__':
    # Test get_relevant_documents
    engine = create_cloud_sql_database_connection()
    embedding = get_embeddings()
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)
    documents = get_relevant_documents("large language modelss", vector_store)
    assert len(documents) > 0, "No documents found for the query"

    # Test format_relevant_documents
    doc_str: str = format_relevant_documents(documents)
    assert len(doc_str) > 0, "No documents formatted successfully"

    print("All tests passed successfully.")