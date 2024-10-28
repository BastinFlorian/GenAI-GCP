"""
List all the files in the bucket
Download a file locally
Load the content of the file with unstructured
Merge the content of the file by page
Create a table if the table doesn't exist
Get embeddings methods
Ingest the data into the table
Create a store instance
"""
import os
import asyncio
import aiohttp 

from sqlalchemy.exc import ProgrammingError
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from langchain_core.documents.base import Document
from langchain_google_cloud_sql_pg import PostgresEngine, PostgresVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_unstructured import UnstructuredLoader
from dotenv import load_dotenv
from config import PROJECT_ID, REGION, INSTANCE, DATABASE, BUCKET_NAME, DB_USER

load_dotenv()
# Sensitive information goes in .env
DB_PASSWORD = os.environ["DB_PASSWORD"]

DOWNLOADED_LOCAL_DIRECTORY = './downloaded_files'


def list_files_in_bucket(bucket:Bucket, directory_name: str = 'data/') -> list[str]:
    """
    List all the files in the specified Google Cloud Storage bucket.

    Args:
        client (storage.Client): The Google Cloud Storage client.
        bucket_name (Bucket): The name of the bucket to list files from.
        directory_name (str, optional): The directory within the bucket to list files from. Defaults to 'data/'.

    Returns:
        list[str]: A list of file names in the specified bucket.
    """
    blobs = bucket.list_blobs(prefix=directory_name)
    return [blob.name for blob in blobs]


def download_file_from_bucket(bucket: Bucket, file_path: str, download_directory_path) -> str:
    """
    Downloads a file from a Google Cloud Storage bucket to a local directory.

    Args:
        bucket (Bucket): The Google Cloud Storage bucket object.
        file_path (str): The path to the file within the bucket.
        download_directory_path (str): The local directory path where the file will be downloaded.

    Returns:
        str: The local file path where the file has been downloaded.

    Raises:
        google.cloud.exceptions.NotFound: If the file does not exist in the bucket.
        google.cloud.exceptions.GoogleCloudError: If there is an error during the download process.

    Example:
        local_path = download_file_from_bucket(bucket, 'path/to/file.txt', '/local/download/directory')
    """
    blob =bucket.get_blob(file_path)
    local_file_name = os.path.basename(file_path)
    local_filepath = os.path.join(download_directory_path, local_file_name)
    blob.download_to_filename(local_filepath)
    print(f"Downloaded '{file_path}' to '{local_file_name}'")
    return local_filepath


def read_file_from_local(local_filepath: str) -> list[Document]:
    """
    Reads a file from the local filesystem and returns a list of Document objects.

    Args:
        local_filepath (str): The path to the local file to be read.

    Returns:
        list[Document]: A list of Document objects loaded from the specified file.
    """
    loader = UnstructuredLoader(local_filepath)
    return loader.load()


def merge_documents_by_page(documents: list[Document]) -> list[Document]:
    """
    Merges a list of Document objects by their page number.

    Args:
        documents (list[Document]): A list of Document objects to be merged. Each Document should have a 'page_number' in its metadata.

    Returns:
        list[Document]: A list of merged Document objects, where each Document contains the concatenated content of all documents with the same page number.
    """
    return"\n".join(doc.page_content for doc in documents)



def create_cloud_sql_database_connection() -> PostgresEngine:
    """
    Establishes a connection to a Cloud SQL PostgreSQL database instance.

    Returns:
        PostgresEngine: An instance of PostgresEngine connected to the specified Cloud SQL database.

    Raises:
        SomeException: Description of the exception that might be raised (if applicable).

    Example:
        connection = create_cloud_sql_database_connection()
    """
    # Connect to the PostgreSQL database
    try:
        engine1 = PostgresEngine.from_instance(
            project_id=PROJECT_ID,
            instance=INSTANCE,
            region=REGION,
            database=DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        print("Successfully connected to the PostgreSQL Cloud SQL instance.")
        return engine1
    except Exception as e:
        print(f"Failed to connect to the PostgreSQL Cloud SQL instance: {e}")
        raise



async def create_table_if_not_exists(table_name: str, engine: PostgresEngine) -> None:
    """
    Creates a table in the vector store if it does not already exist.

    This function attempts to initialize a vector store table with the specified
    table name and a vector size of 768, which is suitable for the VertexAI model
    (textembedding-gecko@latest). If the table already exists, it catches the
    ProgrammingError and prints a message indicating that the table is already created.

    Args:
        table_name (str): The name of the table to be created.
        engine (PostgresEngine): The database engine to create the table in.

    Raises:
        ProgrammingError: If the table already exists.
    """
    try:
        await engine.ainit_vectorstore_table(
                                                table_name=table_name,
                                                vector_size=768,
                                             )  
    except ProgrammingError:
        print("Table already created")

def get_embeddings() -> VertexAIEmbeddings:
    """
    Retrieves the VertexAIEmbeddings instance for the specified model.

    Returns:
        VertexAIEmbeddings:
            An instance of VertexAIEmbeddings configured with the specified model and project.

    Example:
        embeddings = get_embeddings()
    """
    embedding = VertexAIEmbeddings(
                                        model_name='textembedding-gecko@latest',
                                        project=PROJECT_ID
                                    )
    return embedding

def get_vector_store(engine: PostgresEngine, 
                     table_name: str, embedding: VertexAIEmbeddings
                     ) -> PostgresVectorStore:
    """
    Retrieves the vector store from the specified database engine.

    Args:
        engine (PostgresEngine): The database engine to retrieve the vector store from.
        table_name (str): The name of the table to retrieve the vector store from.
        embedding (VertexAIEmbeddings): The VertexAIEmbeddings instance to use for the vector store.

    Returns:
        VectorStore: The vector store object.

    Example:
        vector_store = get_vector_store(engine, 'my_table', embedding)
    """
    return PostgresVectorStore.create_sync(  
        engine=engine,
        table_name=table_name,
        embedding_service=embedding,
    )


async def main():
    async with aiohttp.ClientSession() as session:  #
        client = storage.Client()
        print(BUCKET_NAME)
        bucket = client.get_bucket(BUCKET_NAME)
        files = list_files_in_bucket(bucket)
        assert len(files) > 0, "No files found in the bucket"

        file_path = "data/1 - Gen AI - Dauphine Tunis.pptx"
        download_file_from_bucket(bucket, file_path, DOWNLOADED_LOCAL_DIRECTORY)
        assert os.path.exists(os.path.join(
                                            DOWNLOADED_LOCAL_DIRECTORY,
                                            os.path.basename(file_path))
                                        ), "File not downloaded successfully"

        documents = read_file_from_local(os.path.join(
                                                        DOWNLOADED_LOCAL_DIRECTORY,
                                                        os.path.basename(file_path))
                                                        )
        assert len(documents) > 0, "No documents loaded from the file"

        merged_documents = merge_documents_by_page(documents)
        assert len(merged_documents) > 0, "No documents merged successfully"

        engine = create_cloud_sql_database_connection()
        assert engine is not None, "Database connection not established successfully"

        table_name = "Mehyar_table"
        await create_table_if_not_exists(table_name, engine)

        embeddings = get_embeddings()
        assert embeddings is not None, "Embeddings not retrieved successfully"

        vector_store = get_vector_store(engine, table_name, embeddings)
        assert vector_store is not None, "Vector store not retrieved successfully"
        session.close()


        print("All tests passed successfully!")

if __name__ == '__main__':
    asyncio.run(main())