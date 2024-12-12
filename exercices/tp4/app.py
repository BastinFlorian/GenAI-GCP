"""
Streamlit and FastAPI Integration Application.

This module serves as the entry point for the Streamlit front-end and
FastAPI back-end. It provides a chatbot interface for users to interact
with a document retrieval and question-answering system.

Modules:
    - FastAPI: Handles API requests for document retrieval and answer
      generation.
    - Streamlit: Provides the front-end interface for user interactions.
"""

from urllib.parse import urljoin
from typing import Dict, List

import streamlit as st
import requests


# Define the host for the API
HOST = "https://bilelguembri-api-tp4-1021317796643.europe-west1.run.app"  # Local API


def main():
    """
    Main function to run the Streamlit chatbot application.
    """
    # Set the title of the application
    st.title('Chatbot with Relevant Sources')

    # Sidebar configuration
    with st.sidebar:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.05
        )
        language = st.selectbox(
            'Language',
            ['English', 'Francais', 'Arabic']
        )

    # Initialize session state for storing chat messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "What is your question?"}
        ]

    # Display chat messages from the session state
    for message in st.session_state.messages:
        bot_avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
        st.chat_message(message["role"], avatar=bot_avatar).write(
            message["content"]
        )

    # Handle user input
    if question := st.chat_input("What is your question?"):
        # Append the user's question to the session state messages
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )
        st.chat_message("user", avatar="🧑‍💻").write(question)

        # API call to get an answer
        try:
            # Call the /answer endpoint
            answer_response = requests.post(
                urljoin(HOST, "/answer"),
                json={
                    "question": question,
                    "temperature": temperature,
                    "language": language
                },
                timeout=20
            )

            # Handle the response from the /answer endpoint
            if answer_response.status_code == 200:
                answer = answer_response.json().get(
                    "message", "No answer available."
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                st.chat_message("assistant", avatar="🤖").write(answer)
            else:
                st.error("Error: Unable to get answer from API.")
                st.write(f"Response status: {answer_response.status_code}")
                st.json(answer_response.json())

            # Call the /get_sources endpoint
            sources_response = requests.post(
                urljoin(HOST, "/get_sources"),
                json={
                    "question": question,
                    "temperature": temperature,
                    "language": language
                },
                timeout=20
            )

            # Handle the response from the /get_sources endpoint
            if sources_response.status_code == 200:
                sources: List[Dict[str, str]] = sources_response.json()
                st.write("### Relevant Sources")
                for idx, source in enumerate(sources):
                    with st.expander(f"Source {idx + 1}"):
                        st.write("**Metadata:**")
                        st.json(source.get("metadata", {}))
                        st.write("**Content:**")
                        st.write(source.get("page_content", "No content."))
            else:
                st.error("Error: Unable to get sources from API.")
                st.write(f"Response status: {sources_response.status_code}")
                st.json(sources_response.json())

        except requests.exceptions.RequestException as e:
            st.error(f"API connection error: {e}")


if __name__ == "__main__":
    main()
