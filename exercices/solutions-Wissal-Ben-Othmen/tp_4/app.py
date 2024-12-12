"""
Streamlit chatbot application with API integration and source retrieval.

This module creates a chatbot interface using Streamlit
that connects to a local API
to fetch answers and relevant sources for user questions.
"""
from urllib.parse import urljoin
from typing import Dict, List
import streamlit as st
import requests


# Define the host for the API
HOST = "https://wissal-api-1021317796643.europe-west1.run.app"

# Set the title of the application
st.title('Chatbot with Relevant Sources')

# Sidebar configuration
with st.sidebar:
    TEMPERATURE = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05
    )
    LANGUAGE = st.selectbox(
        'Language', ['English', 'Francais', 'Arabic'],
    )

# Initialize session state for storing chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question?"}
    ]

# Display chat messages from the session state
for n, message in enumerate(st.session_state.messages):
    USER_AVATAR = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    # Display the chat message with the specified role and avatar
    st.chat_message(
        message["role"],
        avatar=USER_AVATAR
    ).write(message["content"])

# Handle user input
if question := st.chat_input("What is your question?"):
    # Append the user's question to the session state messages
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    # API call to get an answer
    try:
        # Call the /answer endpoint
        answer_response = requests.post(
            urljoin(HOST, "/answer"),
            json={
                "question": question,
                "temperature": TEMPERATURE,
                "language": LANGUAGE,
            },
            timeout=20,
        )

        # Call the /get_sources endpoint
        sources_response = requests.post(
            urljoin(HOST, "/get_sources"),
            json={
                "question": question,
                "temperature": TEMPERATURE,
                "language": LANGUAGE,
            },
            timeout=20,
        )

        # Handle the response from the /answer endpoint
        if answer_response.status_code == 200:
            answer = answer_response.json().get(
                                                    "message",
                                                    "No answer provided."
                                                )
            st.session_state["messages"].append(
                {"role": "assistant", "content": answer}
            )
            st.chat_message("assistant", avatar="🤖").write(answer)
        else:
            st.error("Error: Unable to get a response from the 'answer' API.")
            st.write(f"Response status: {answer_response.status_code}")
            st.write(f"Error message: {answer_response.text}")

        # Handle the response from the /get_sources endpoint
        if sources_response.status_code == 200:
            sources: List[Dict[str, str]] = sources_response.json()
            st.write("### Relevant Sources")
            for i, source in enumerate(sources):
                with st.expander(f"Source {i + 1}"):
                    st.write("**Metadata:**")
                    st.json(source.get("metadata", {}))
                    st.write("**Content:**")
                    st.write(
                            source.get("page_content", "No content available.")
                        )
        else:
            st.error(
                "Error: Unable to get a response from the 'get_sources' API."
            )
            st.write(f"Response status: {sources_response.status_code}")
            st.write(f"Error message: {sources_response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while connecting to the API: {e}")
# [missing-final-newline]
