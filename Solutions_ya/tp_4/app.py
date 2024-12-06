"""Streamlit app"""

from typing import Dict, List
import streamlit as st
import requests


from google.cloud import storage
from config import BUCKET_NAME
from ingest import list_files_in_bucket

# HOST = "http://0.0.0.0:8181/answer"  # Docker run name of Fast API
HOST = "http://127.0.0.1:8181"

client = storage.Client()


st.title("Chatbot")


with st.sidebar:
    st.header("Settings")
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05
    )
    similarity_threshold = st.slider(
        "RAG Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05,
        disabled=True,
    )
    language = st.selectbox("language", ["English", "Francais", "Arabic"])

    st.subheader(f"Ingested Files ({BUCKET_NAME})")
    try:
        bucket = client.get_bucket(BUCKET_NAME)
        files = list_files_in_bucket(client, bucket)
        for i, file in enumerate(files):
            if i != 0:
                st.write(file[5:])
    except Exception as e:
        st.error(f"Failed to fetch files: {e}")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How may I help you?", "sources": []}
    ]


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




if question := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    documents = requests.post(
        f"{HOST}/get_sources",
        json={
            "question": question,
            "temperature": temperature,
            "similarity_threshold": similarity_threshold,
            "language": language,
            "documents": [],
            "previous_context": [],
        },
        timeout=30,
    )
    docs = documents.json()

    if not isinstance(docs, list):
        docs = []

    response = requests.post(
        f"{HOST}/answer",
        json={
            "question": question,
            "temperature": temperature,
            "similarity_threshold": similarity_threshold,
            "language": language,
            "documents": docs,
            "previous_context": st.session_state["messages"],
        },
        timeout=30,
    )

    if response.status_code == 200:
        answer = response.json()
        st.session_state.messages.append(
            {"role": "assistant", "content": answer["message"], "sources": []}
        )
        st.chat_message("assistant", avatar="🤖").write(answer["message"])
    else:
        st.write("Error: Unable to get a response from the API (response)")
        st.write(f"The error is: {response.text}\nStatus Code: {response.status_code}")
    if documents.status_code == 200:
        st.session_state.messages[-1][
            "sources"
        ] = docs  # Attach sources to last answer
        for i, source in enumerate(documents):
            with st.expander(
                f"Source {i+1}"
            ):
                st.write("Metadata:")
                st.write(source.metadata)
                st.write("Content:")
                st.write(source.page_content)
    else:
        st.write("Error: Unable to get a response from the API (documents)")
        st.write(f"The error is: {documents.text}\nStatus Code: {documents.status_code}")