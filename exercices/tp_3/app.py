"""
Streamlit application for generating short stories using a FastAPI backend.
"""

import streamlit as st
import requests

# Set the host URL for the FastAPI endpoint
HOST = "https://bilelguembri-api-tp3-1021317796643.europe-west1.run.app/answer"

st.title('AI Short Story Generator')

# Sidebar options
with st.sidebar:
    # Temperature selection slider
    temperature = st.slider(
        "Select response creativity (temperature)",
        0.0,
        1.0,
        0.7
    )

    # Language selection
    language = st.selectbox(
        "Select story language",
        ["English", "French", "Arabic"]
    )

# Initialize the chat history if it doesn't exist in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Enter a theme for your short story, "
                "and I’ll create one for you!"
            )
        }
    ]

# Display the chat history
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# Chat input box
if user_theme := st.chat_input("Enter a theme for your story"):
    # Append user's theme to the chat history
    st.session_state["messages"].append({
        "role": "user",
        "content": user_theme
    })

    # Display the user's theme in the chat
    st.chat_message("user").write(user_theme)

    # Create the payload for the FastAPI request
    payload = {
        "question": user_theme,
        "temperature": temperature,
        "language": language
    }

    # Send request to FastAPI endpoint
    try:
        response = requests.post(
            HOST,
            json=payload,
            timeout=20
        )

        # Process response
        if response.status_code == 200:
            assistant_reply = response.json().get(
                "message",
                "No response from API"
            )
            st.session_state["messages"].append({
                "role": "assistant",
                "content": assistant_reply
            })
            st.chat_message("assistant").write(assistant_reply)
        else:
            st.chat_message("assistant").write(
                "Error: Unable to get a response from the API"
            )

    except requests.ConnectionError as e:
        st.chat_message("assistant").write(f"Connection error: {e}")
