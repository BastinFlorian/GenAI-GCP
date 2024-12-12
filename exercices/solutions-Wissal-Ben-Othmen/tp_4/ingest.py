"""
Ingest script for processing documents from Google Cloud Storage,
embedding them using VertexAI, and creating a FAISS vector store.
"""

import os
from dotenv import load_dotenv
from google.cloud import storage
from langchain_core.documents.base import Document
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores import FAISS

load_dotenv()

# Environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
BUCKET_NAME = "dauphine-bucket"

DOWNLOADED_LOCAL_DIRECTORY = './downloaded_files'


def list_files_in_bucket(gcs_client: storage.Client,
                         bucket_name: str,
                         directory_name: str = 'data/') -> list[str]:
    """
    List all the files in the specified Google Cloud Storage bucket.

    Args:
        gcs_client (storage.Client): The Google Cloud Storage client.
        bucket_name (str): The name of the bucket to list files from.
        directory_name (str, optional): The directory within the bucket
            to list files from. Defaults to 'data/'.

    Returns:
        list[str]: A list of file names in the specified bucket.
    """
    gcs_bucket = gcs_client.bucket(bucket_name)
    blobs = gcs_bucket.list_blobs(prefix=directory_name)
    return [blob.name for blob in blobs]


def download_file_from_bucket(gcs_bucket: storage.Bucket,
                              remote_path: str,
                              local_directory: str) -> str:
    """
    Downloads a file from a Google Cloud Storage bucket to a local directory.

    Args:
        gcs_bucket (storage.Bucket): The Google Cloud Storage bucket object.
        remote_path (str): The path to the file within the bucket.
        local_directory (str): The local directory path for the download.

    Returns:
        str: The local file path of the downloaded file.
    """
    blob = gcs_bucket.blob(remote_path)
    local_filename = os.path.basename(remote_path)
    local_filepath = os.path.join(local_directory, local_filename)
    blob.download_to_filename(local_filepath)
    print(f"Downloaded '{remote_path}' to '{local_filepath}'")
    return local_filepath


def read_file_from_local(filepath: str) -> list[Document]:
    """
    Reads a file from the local filesystem and loads it into Document objects.

    Args:
        filepath (str): Path to the local file.

    Returns:
        list[Document]: A list of Document objects from the file.
    """
    loader = UnstructuredLoader(filepath)
    loaded_documents = loader.load()

    for doc in loaded_documents:
        if not doc.metadata:
            doc.metadata = {"source": filepath}

    return loaded_documents


def merge_documents_by_page(docs: list[Document]) -> list[Document]:
    """
    Merges Document objects by their page number.

    Args:
        docs (list[Document]): Documents to merge.

    Returns:
        list[Document]: Merged documents with concatenated content.
    """
    documents_by_page = {}
    for doc in docs:
        page = doc.metadata.get('page_number', 0)
        if page not in documents_by_page:
            documents_by_page[page] = []
        documents_by_page[page].append(doc)

    result_docs = []
    for page, page_docs in documents_by_page.items():
        content = '\n'.join(doc.page_content for doc in page_docs)
        metadata = page_docs[0].metadata.copy()
        result_docs.append(Document(page_content=content, metadata=metadata))

    return result_docs


def get_embeddings() -> VertexAIEmbeddings:
    """
    Retrieves a VertexAIEmbeddings instance for the specified model.

    Returns:
        VertexAIEmbeddings: Configured embeddings instance.
    """
    return VertexAIEmbeddings(
        model_name="textembedding-gecko@latest",
        project=PROJECT_ID,
    )


def create_vector_store(docs: list[Document]) -> FAISS:
    """
    Creates a FAISS vector store from text chunks using VertexAI embeddings.

    Args:
        docs (list[Document]): List of Document objects.

    Returns:
        FAISS: Vector store with embedded document chunks.
    """
    embeddings = VertexAIEmbeddings(
        project=PROJECT_ID,
        location=REGION,
        model_name="textembedding-gecko-multilingual@latest"
    )

    text_chunks = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    faiss_store = FAISS.from_texts(
        text_chunks, embedding=embeddings, metadatas=metadatas
    )
    faiss_store.save_local("faiss_index")
    return faiss_store


if __name__ == '__main__':
    os.makedirs(DOWNLOADED_LOCAL_DIRECTORY, exist_ok=True)

    client = storage.Client()
    files_in_bucket = list_files_in_bucket(client, BUCKET_NAME)
    if not files_in_bucket:
        raise RuntimeError("No files found in the bucket.")

    FILE_PATH = "data/1 - Gen AI - Dauphine Tunis.pptx"
    bucket = client.bucket(BUCKET_NAME)
    local_file = download_file_from_bucket(bucket, FILE_PATH,
                                           DOWNLOADED_LOCAL_DIRECTORY)

    documents = read_file_from_local(local_file)
    if not documents:
        raise RuntimeError("Failed to load documents from file.")

    merged_docs = merge_documents_by_page(documents)
    if not merged_docs:
        raise RuntimeError("No documents after merging.")

    vector_store = create_vector_store(merged_docs)
    if not vector_store:
        raise RuntimeError("Vector store creation failed.")

    print("All tasks completed successfully.")

# End-of-file (EOF)
