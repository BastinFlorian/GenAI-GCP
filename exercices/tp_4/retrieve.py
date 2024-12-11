import os
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_core.documents.base import Document
from config import TABLE_NAME

# fonction pour récupérer les documents pertinents en fonction d'une requête définie
# et un vector store


def get_relevant_documents(
        query: str, vector_store: PostgresVectorStore
        ) -> list[Document]:
    """
    Retrieve relevant documents based on a query using a vector store.

    Args:
        query (str): The search query string.
        vector_store (PostgresVectorStore): An instance of PostgresVectorStore used to retrieve documents.
    Returns:
        list[Document]: A list of documents relevant to the query.
    """
    # effectue une recherche de similarité avec des scores de pertinence
    results = vector_store.similarity_search_with_relevance_scores(
        query=query, k=4
        )

    # vérifie si les résultats contiennent des scores ou non
    if results and isinstance(results[0], Document):
        # suppose que tous les documents sont pertinents s'il n'y a pas de scores
        relevant_docs = results  # Assume documents are relevant if no scores
    else:
        # filtre uniquement les documents ayant un score supérieur ou égal à 0.6
        relevant_docs = [doc for doc, score in results if score >= 0.6]
    for doc in relevant_docs:
        doc.metadata["score"] = doc.metadata.get("score", "N/A")  # Add a default score
    return relevant_docs


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
    return "\n".join([f"Source {i+1}: {doc.page_content}" for i, 
                      doc in enumerate(documents)])


if __name__ == '__main__':
    # Test get_relevant_documents
    engine = create_cloud_sql_database_connection()
    # charge les embeddings utilisés pour représenter les documents et requêtes
    embedding = get_embeddings()
    # Configure le vector store en se connectant à la base de données sql,
    # en spécifiant le nom de la table et les embeddings à utiliser
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)
    documents = get_relevant_documents("large language modelss", vector_store)
    assert len(documents) > 0, "No documents found for the query"

    # Test format_relevant_documents
    doc_str: str = format_relevant_documents(documents)
    assert len(doc_str) > 0, "No documents formatted successfully"

    print("All tests passed successfully.")
