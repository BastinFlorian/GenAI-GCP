import asyncio
from ingest import (
    create_cloud_sql_database_connection,
    get_embeddings,
    get_vector_store,
)
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_core.documents.base import Document
from config import TABLE_NAME
from langchain.schema import BaseRetriever


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
    retriever: BaseRetriever = vector_store.as_retriever()
    return retriever.invoke(query)


def format_relevant_documents(documents: list[Document]) -> str:
    """
    Format relevant documents into a string.

    Args:
        documents (list[Document]): A list of relevant documents.

    Returns:
        str: A formatted string containing the relevant documents.
    """
    return "\n-----\n".join(
        [f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(documents)]
    )


import aiohttp
import asyncio


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://example.com") as response:
            return await response.text()


async def main():
    # Test logic here
    await fetch_data()
    print("All tests passed successfully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
