import streamlit as st
import requests
from typing import Dict, List

HOST = "https://dt4api-1021317796643.europe-west1.run.app"

st.title("Donia Chatbot")

if "files_fetched" not in st.session_state:
    st.session_state.files_fetched = False
    st.session_state.files = []

if not st.session_state.files_fetched:
    try:
        response = requests.post(f"{HOST}/get_files_names", timeout=30)
        files = response.json().get("files", [])
        if files:
            st.session_state.files = files
            st.session_state.files_fetched = True
        else:
            st.info("No files found in the bucket.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch files: {e}")

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
    similarity_threshold = st.slider("RAG Similarity Threshold", 0.0, 1.0, 0.50, 0.05)
    language = st.selectbox("Language", ["English", "Francais", "Arabic"])
    st.subheader("Ingested Files")
    for file in st.session_state.files[1:]:
        st.write(file[5:])

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How may I help you?"}]

for n, message in enumerate(st.session_state.messages):
    st.chat_message(message["role"]).write(message["content"])

if question := st.chat_input("Tap your question here:"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    documents = requests.post(
        f"{HOST}/get_sources",
        json={"question": question, "temperature": temperature, "similarity_threshold": similarity_threshold, "language": language, "documents": [], "previous_context": st.session_state["messages"]},
        timeout=30,
    )

    if documents.status_code == 200:
        response = requests.post(
            f"{HOST}/answer",
            json={"question": question, "temperature": temperature, "similarity_threshold": similarity_threshold, "language": language, "documents": documents.json(), "previous_context": st.session_state["messages"]},
            timeout=30,
        )

        if response.status_code == 200:
            answer = response.json()["message"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
        else:
            st.error("Error: Unable to get a response from the API (answer)")
    else:
        st.error("Error: Unable to get a response from the API (documents)")
