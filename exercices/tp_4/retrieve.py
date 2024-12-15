import os
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_core.documents.base import Document
from config import TABLE_NAME



def get_relevant_documents(query: str, vector_stored: PostgresVectorStore) -> list[Document]:
    """
    Retrieve the most relevant documents for a given query using Maximal Marginal Relevance (MMR).

    Args:
        query (str): The user-provided input query for retrieving documents.
        vector_stored (PostgresVectorStore): A vector-based storage system for document embeddings.

    Returns:
        list[Document]: A list of the top `k` relevant documents, optimized for both relevance and diversity.
    """
    retriever = vector_stored.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'lambda_mult': 0.25}
    )
    # Filter and normalize scores to ensure relevance between 0 and 1
    documents_with_scores = retriever.invoke(query)
    return documents_with_scores



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
    return "\n-----\n".join([f"Source {i + 1}: {doc.page_content}"for i, doc in enumerate(documents)])


if __name__ == '__main__':
    
    Example_de_test = """
    What are the differences between LSTM and GRU in handling vanishing gradients?
    How does the self-attention mechanism work in transformers? 
    Looking for examples and formulas for understanding attention scores.
"""
    # Test get_relevant_documents
    engine = create_cloud_sql_database_connection()
    embedding = get_embeddings()
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)    
    documents = get_relevant_documents(Example_de_test, vector_store)
    assert len(documents) > 0, "No documents found for the query"

    # Test format_relevant_documents
    doc_str: str = format_relevant_documents(documents)
    assert len(doc_str) > 0, "No documents formatted successfully"

    print("All tests passed successfully.")