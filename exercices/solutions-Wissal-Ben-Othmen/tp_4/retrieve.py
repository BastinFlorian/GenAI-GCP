"""
Document retrieval script using FAISS vector store and VertexAI embeddings.
Allows interactive querying of embedded documents
with configurable result count.
"""

import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.documents.base import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")


def initialize_vector_store() -> FAISS:
    """
    Load the FAISS vector store from disk.

    Returns:
        FAISS: The loaded vector store.
    """
    embeddings = VertexAIEmbeddings(
        project=PROJECT_ID,
        location=REGION,
        model_name="textembedding-gecko-multilingual@latest"
    )

    # Load the FAISS index from the local file
    faiss_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return faiss_store


def search_documents(
    search_query: str,
    faiss_store: FAISS,
    num_results: int = 4
) -> List[Document]:
    """
    Retrieve relevant documents based on a query using a vector store.

    Args:
        search_query (str): The search query string.
        faiss_store (FAISS): The FAISS vector store to search in.
        num_results (int, optional): Number of documents to retrieve.
        Defaults to 4.

    Returns:
        List[Document]: A list of documents relevant to the query.
    """
    documents = faiss_store.similarity_search(
        query=search_query, k=num_results)
    # Check and ensure metadata is present for each document
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {"source": "Unknown"}
    return documents


def format_relevant_documents(documents: List[Document]) -> str:
    """
    Format relevant documents into a readable string.

    Args:
        documents (List[Document]): A list of relevant documents.

    Returns:
        str: A formatted string containing all relevant documents.
    """
    formatted_docs = []
    for i, doc in enumerate(documents, 1):
        content = doc.page_content.strip().replace("\n\n", "\n")
        doc_str = (
            f"\n[Source {i}]\n"
            f"Metadata:\n{doc.metadata}\n"
            f"Content:\n{content}"
        )
        formatted_docs.append(doc_str)

    return "\n\n" + "=" * 50 + "\n".join(formatted_docs)


if __name__ == '__main__':
    # Load the vector store
    print("Loading vector store...")
    vector_store = initialize_vector_store()
    print("Vector store loaded successfully!")

    while True:
        # Get query from user
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() in ['quit', 'exit', 'q']:
            break

        # Get number of results
        try:
            k = int(
                input("How many results do you want? (default: 4): ") or "4"
            )
        except ValueError:
            k = 4

        # Get relevant documents
        print("\nSearching...")
        relevant_docs = search_documents(
            search_query=query,
            faiss_store=vector_store,
            num_results=k
        )

        # Format and print results
        print(f"\nResults for: '{query}'")
        print(format_relevant_documents(relevant_docs))
        print("\nIgnore any gRPC shutdown warnings - they don't affect "
              "functionality.")

    print("\nThank you for using the document search! Goodbye!")
# End-of-file (EOF)
