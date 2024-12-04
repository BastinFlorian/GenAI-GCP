import os
import requests
import streamlit as st
from typing import Dict, List


HOST = "http://127.0.0.1:8181"  # Docker run name of FastAPI
#HOST = "https://mjb-api-1021317796643.europe-west1.run.app" # Cloud Run

# Page Configuration
st.set_page_config(page_title="AI Chatbot Assistant", page_icon="🤖", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .stSidebar {background-color: #F0F8FF;}
    .stButton > button {background-color: #1E90FF; color: white;}
    .stMarkdown {font-family: Arial, sans-serif;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with Icon
st.title("🤖 AI Chatbot Assistant")

# Sidebar for Settings
with st.sidebar:
    st.markdown("### 🔧 Settings")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    language = st.selectbox("Language", ["English", "Francais", "Arabic"])

# Initialize messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What is your question?"}]

# Display previous messages
st.markdown("### 💬 Chat History")
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    st.chat_message(message["role"], avatar=avatar).write(message["content"])

# Handle user input
if question := st.chat_input("What is your question?"):
    # Append the question from the user to session state
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    try:
        # Show spinner while processing
        with st.spinner("🤖 Generating response..."):
            # Fetch documents related to the question
            documents = requests.post(
                f"{HOST}/get_sources",
                json={
                    "question": question,
                    "temperature": temperature,
                    "language": language,
                    "documents": [],
                    "previous_context": [],
                },
                timeout=30,
            )
            documents.raise_for_status()  # Raise exception for non-2xx responses
            docs = documents.json()

            if not isinstance(docs, list):
                docs = []  # Default to empty list if response is not in the expected format

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching documents: {e}")
        docs = []

    try:
        # Fetch the answer based on the question and the documents
        response = requests.post(
            f"{HOST}/answer",
            json={
                "question": question,
                "temperature": temperature,
                "language": language,
                "documents": docs,
                "previous_context": st.session_state["messages"],
            },
            timeout=30,
        )
        response.raise_for_status()  # Raise exception for non-2xx responses

        if response.status_code == 200:
            answer = response.json().get("message", "No message returned")
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.chat_message("assistant", avatar="🤖").write(answer)
        else:
            st.write("Error: Unable to get a response from the API")
            st.write(f"The error is: {response.text}")

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching answer: {e}")

    # Display sources if documents were fetched
    if docs:
        st.markdown("### 📚 Sources")
        for i, source in enumerate(docs):
            with st.expander(f"Source {i+1}"):
                st.write("**Metadata:**")
                st.write(source.get("metadata", "No metadata available"))
                st.write("**Content:**")
                st.write(source.get("page_content", "No content available"))
    else:
        st.write("No sources available.")

# Footer Section
st.markdown("---")
st.markdown("© 2024, Jihed Bhar. Powered by AI. 🧠")
