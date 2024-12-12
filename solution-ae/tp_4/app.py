import os
from typing import Dict, List
import streamlit as st
import requests
from google.cloud import storage
from config import BUCKET_NAME
from ingest import list_files_in_bucket

# Initialize the Google Cloud Storage client
client = storage.Client()


#HOST = "http://localhost:8181"  # Docker run name of Fast API
#HOST = "http://0.0.0.0:8181/answer"

HOST = "https://ae-api-1021317796643.europe-west1.run.app"  # Cloud Run

st.title('Hello, Streamlit!')

# Initialize session state variables
if "files" not in st.session_state:
    st.session_state["files"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What is your question?"}]

with st.sidebar:
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    language = st.selectbox('Language', ['English', 'Francais', 'Arabic'])

    st.subheader(f"Ingested Files ({BUCKET_NAME})")
    try:
        bucket = client.get_bucket(BUCKET_NAME)
        st.session_state.files = list_files_in_bucket(client, bucket)
        for i, file in enumerate(st.session_state.files):
            if i != 0:
                st.write(file[5:])
    except Exception as e:
        st.error(f"Failed to fetch files: {e}")

# Display chat messages
for n, message in enumerate(st.session_state.messages):
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    st.chat_message(message["role"], avatar=avatar).write(message["content"])
    if "sources" in message and message["sources"]:
        for i, source in enumerate(message["sources"]):
            with st.expander(f"Source {i+1}"):
                st.write("Metadata:")
                st.write(source["metadata"])
                st.write("Content:")
                st.write(source["page_content"])

# Handle user input and API requests
if question := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    # API request for answer
    response = requests.post(
        f"{HOST}/answer",
        json={
            "question": question,
            "temperature": temperature,
            "language": language,
            "documents": [],  # Ensure this is an empty list to initialize if not set
            "previous_context": st.session_state["messages"],
        },
        timeout=20,
    )

    # API request for documents
    documents = requests.post(
        f"{HOST}/get_sources", 
        json={
            "question": question,
            "temperature": temperature,
            "language": language
        },
        timeout=30
    )

    # Handle API responses
    if response.status_code == 200:
        answer = response.json()["message"]
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("user", avatar="🤖").write(answer)
    else:
        st.error(f"Error: Unable to get a response from the API. The error is: {response.text}")

    if documents.status_code == 200:
        sources: List[Dict[str, str]] = documents.json()
        for i, source in enumerate(sources):
            with st.expander(f"Source {i+1}"):
                st.write("Metadata:")
                st.write(source["metadata"])
                st.write("Content:")
                st.write(source["page_content"])
    else:
        st.error(f"Error: Unable to get a response from the API. The error is: {documents.text}")
