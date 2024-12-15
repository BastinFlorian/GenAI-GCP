import os
from dotenv import load_dotenv
from sqlalchemy.exc import ProgrammingError
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from langchain_core.documents.base import Document
from langchain_google_cloud_sql_pg import PostgresEngine, PostgresVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_unstructured import UnstructuredLoader
from config import PROJECT_ID, REGION, INSTANCE, DATABASE, BUCKET_NAME, DB_USER

load_dotenv()
DB_PASSWORD = os.environ["DB_PASSWORD"]
DOWNLOADED_LOCAL_FIRECTORY = './downloaded_files'

def list_files_in_bucket(client: storage.Client, bucket_name: Bucket, directory_name: str = 'data/') -> list[str]:
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=directory_name)
    return [blob.name for blob in blobs]

def download_file_from_bucket(bucket: Bucket, file_path: str, download_directory_path) -> str:
    blob = bucket.blob(file_path)
    local_file_name = os.path.basename(file_path)
    local_filepath = os.path.join(download_directory_path, local_file_name)
    blob.download_to_filename(local_filepath)
    print(f"Downloaded '{file_path}' to '{local_file_name}'")
    return local_filepath

def read_file_from_local(local_filepath: str) -> list[Document]:
    loader = UnstructuredLoader(local_filepath)
    documents = loader.load()
    return documents

def merge_documents_by_page(documents: list[Document]) -> list[Document]:
    merged_documents = {}
    for doc in documents:
        page_number = doc.metadata.get("page_number")
        if page_number not in merged_documents:
            merged_documents[page_number] = []
        merged_documents[page_number].append(doc.page_content)

    merged_documents = [
        Document(page_content=" ".join(contents), metadata={"page_number": page})
        for page, contents in merged_documents.items()
    ]
    return merged_documents

def create_cloud_sql_database_connection() -> PostgresEngine:
    engine = PostgresEngine(
        project_id=PROJECT_ID,
        region=REGION,
        instance=INSTANCE,
        database=DATABASE,
        db_user=DB_USER,
        db_password=DB_PASSWORD,
    )
    return engine
##
def create_table_if_not_exists(table_name: str, engine: PostgresEngine) -> None:
    try:
        engine.create_vector_store_table(
            table_name=table_name, vector_size=768
        )
    except ProgrammingError:
        print("Table already created")

def get_embeddings() -> VertexAIEmbeddings:
    return VertexAIEmbeddings(project_id=PROJECT_ID, region=REGION)

def get_vector_store(engine: PostgresEngine, table_name: str, embedding: VertexAIEmbeddings) -> PostgresVectorStore:
    return PostgresVectorStore(engine=engine, table_name=table_name, embedding=embedding)

if __name__ == '__main__':
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)

    files = list_files_in_bucket(client, bucket)
    assert len(files) > 0, "No files found in the bucket"

    file_path = "data/1 - Gen AI - Dauphine Tunis.pptx"
    download_file_from_bucket(bucket, file_path, DOWNLOADED_LOCAL_FIRECTORY)
    assert os.path.exists(os.path.join(DOWNLOADED_LOCAL_FIRECTORY, os.path.basename(file_path))), "File not downloaded successfully"

    documents = read_file_from_local(os.path.join(DOWNLOADED_LOCAL_FIRECTORY, os.path.basename(file_path)))
    assert len(documents) > 0, "No documents loaded from the file"

    merged_documents = merge_documents_by_page(documents)
    assert len(merged_documents) > 0, "No documents merged successfully"

    engine = create_cloud_sql_database_connection()
    assert engine is not None, "Database connection not established successfully"

    table_name = "my_table"
    create_table_if_not_exists(table_name, engine)

    embeddings = get_embeddings()
    assert embeddings is not None, "Embeddings not retrieved successfully"

    vector_store = get_vector_store(engine, table_name, embeddings)
    assert vector_store is not None, "Vector store not retrieved successfully"

    print("All tests passed successfully!")
