"""
This module handles the ingestion of data from Google Cloud Storage,
including downloading, processing, and creating a vector store for
the documents. It provides functions to list files in a bucket,
download a specific file, read the content of a file, merge documents
by page, and create a FAISS vector store using VertexAI embeddings.
"""
import os
from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from langchain_core.documents.base import Document
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores import FAISS

# Load environment variables from .env file
load_dotenv()

# Get environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
BUCKET_NAME = "dauphine-bucket"  # This is hardcoded in config.py

DOWNLOADED_LOCAL_DIRECTORY = './downloaded_files'


def list_files_in_bucket(
    client: storage.Client, bucket_name: str, directory_name: str = 'data/'
) -> list[str]:
    """List all files in the specified Google Cloud Storage bucket."""
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=directory_name)
    return [blob.name for blob in blobs]


def download_file_from_bucket(
    bucket: Bucket, file_path: str, download_directory_path: str
) -> str:
    """Downloads a file from a GCS bucket to a local directory."""
    blob = bucket.blob(file_path)
    local_file_name = os.path.basename(file_path)
    local_filepath = os.path.join(download_directory_path, local_file_name)
    blob.download_to_filename(local_filepath)
    print(f"Downloaded '{file_path}' to '{local_file_name}'")
    return local_filepath


def read_file_from_local(local_filepath: str) -> list[Document]:
    """Reads a file from local filesystem, returns list of Document."""
    loader = UnstructuredLoader(local_filepath)
    documents = loader.load()

    # Add metadata (e.g., source) to each document
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {"source": local_filepath}

    return documents


def merge_documents_by_page(documents: list[Document]) -> list[Document]:
    """Merges a list of Document objects by their page number."""
    page_groups = {}
    for doc in documents:
        page_number = doc.metadata.get('page_number', 0)
        if page_number not in page_groups:
            page_groups[page_number] = []
        page_groups[page_number].append(doc)

    merged_documents = []
    for page_number, docs in page_groups.items():
        merged_content = '\n'.join(doc.page_content for doc in docs)
        merged_metadata = docs[0].metadata.copy()
        merged_documents.append(
            Document(page_content=merged_content, metadata=merged_metadata)
        )

    return merged_documents


def get_embeddings() -> VertexAIEmbeddings:
    """Retrieves the VertexAIEmbeddings instance."""
    return VertexAIEmbeddings(
        model_name="textembedding-gecko@latest",
        project=PROJECT_ID,
    )


def get_vector_store(documents: list[Document]) -> FAISS:
    """Creates a FAISS vector store from documents using embeddings."""
    embeddings = VertexAIEmbeddings(
        project=PROJECT_ID,
        location=REGION,
        model_name="textembedding-gecko-multilingual@latest"
    )

    # Extract text chunks and metadata
    text_chunks = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]

    # Pass both text chunks and metadata to FAISS
    vector_store = FAISS.from_texts(
        text_chunks, embedding=embeddings, metadatas=metadatas
    )
    vector_store.save_local("faiss_index")
    return vector_store


if __name__ == '__main__':
    # Create download directory if it doesn't exist
    os.makedirs(DOWNLOADED_LOCAL_DIRECTORY, exist_ok=True)

    # Test list_files_in_bucket
    storage_client = storage.Client()
    files = list_files_in_bucket(storage_client, BUCKET_NAME)
    assert len(files) > 0, "No files found in the bucket"

    # Test download_file_from_bucket
    FILE_PATH_ = "data/1 - Gen AI - Dauphine Tunis.pptx"
    bucket_ = storage_client.get_bucket(BUCKET_NAME)
    download_file_from_bucket(
        bucket_, FILE_PATH_, DOWNLOADED_LOCAL_DIRECTORY
    )
    assert os.path.exists(
        os.path.join(DOWNLOADED_LOCAL_DIRECTORY, os.path.basename(FILE_PATH_))
    ), "File not downloaded successfully"

    # Test read_file_from_local
    documents_ = read_file_from_local(
        os.path.join(DOWNLOADED_LOCAL_DIRECTORY, os.path.basename(FILE_PATH_))
    )
    assert len(documents_) > 0, "No documents loaded from the file"

    # Test merge_documents_by_page
    merged_documents_ = merge_documents_by_page(documents_)
    assert len(merged_documents_) > 0, "No documents after merging"

    # Extract text chunks from merged documents
    text_chunks_ = [doc.page_content for doc in merged_documents_]

    # Test get_vector_store with FAISS
    vector_store_ = get_vector_store(merged_documents_)
    assert vector_store_ is not None, "Vector store not created successfully"
    assert os.path.exists(
        "faiss_index"
    ), "FAISS index not saved successfully"
    print("All tests passed successfully!")
