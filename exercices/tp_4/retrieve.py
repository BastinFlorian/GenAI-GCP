"""
This module provides a setup for retrieving relevant documents from a Google Cloud SQL 
database using vector similarity with the LangChain framework. It establishes a connection 
to a Cloud SQL database, retrieves relevant documents based on input queries, and formats 
the output for display. 
"""
from langchain_google_cloud_sql_pg import PostgresVectorStore  # Move third-party imports here
from langchain_core.documents.base import Document
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from config import TABLE_NAME

def get_relevant_documents(query: str, vector_stored: PostgresVectorStore) -> list[Document]:
    """
    Retrieve relevant documents based on similarity scoring.
    
    Args:
        query (str): The input query for document retrieval.
        vector_stored (PostgresVectorStore): The vector store for searching documents.
        
    Returns:
        list[Document]: A list of relevant documents filtered by similarity score.
    """
    retriever = vector_stored.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 6, 'lambda_mult': 0.25}
    )
    # Filter and normalize scores to ensure relevance between 0 and 1
    documents_with_scores = retriever.invoke(query)
    return documents_with_scores

def format_relevant_documents(documents: list[Document]) -> str:
    """
    Format relevant documents into a string.

    Args:
        documents (list[Document]): A list of relevant documents.

    Returns:
        str: A formatted string of relevant documents.
    """
    return "\n-----\n".join(
                                [f"Source {i + 1}: {doc.page_content}" 
                                for i, doc in enumerate(documents)]
                            )

if __name__ == '__main__':
    # Example query text for testing
    QUERY_TEXT = ''' Training RL model\nAlso transformer based 
    LM\nVariation in sizes used (relative to policy)\nOutputs 
    scalar from input text\n Prevent over optimization \n‹#›\nLambert, 
    2022, Illustrating Reinforcement Learning from Human Feedback (RLHF) 
    [Blog]\nII.A.4 LSTM\n Long Short Term Memory (LSTM)\nWhat about Vanishing / 
    Exploding Gradients ? 
    \nThe additive update function for the cell state gives a derivative 
    that is much more ‘well behaved’\nThe gating functions allow the 
    network to decide how much the gradient vanishes, and can take on
      different values at each time step. The values that they take on 
      are learned functions of the current input and hidden state.\n
      To get details on LSTM derivative, check out this blog post \nColah, 
    Understanding LSTM Networks [Blog] \n‹#›\nII.B.1 Self Attention 
    Mechanism\nValue Matrix (12 288, 12 288) decomposition≈\nIdea: \n
    The number of # is 150m for the Value
    '''

    # Test get_relevant_documents
    engine = create_cloud_sql_database_connection()
    embedding = get_embeddings()
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)    
    # Perform similarity search
    retrieved_documents = get_relevant_documents(QUERY_TEXT, vector_store)
    print(TABLE_NAME)
    assert len(retrieved_documents) > 0, "No documents found for the query"

    # Test format_relevant_documents
    doc_str: str = format_relevant_documents(retrieved_documents)
    assert len(doc_str) > 0, "No documents formatted successfully"

    print("All tests passed successfully.")
