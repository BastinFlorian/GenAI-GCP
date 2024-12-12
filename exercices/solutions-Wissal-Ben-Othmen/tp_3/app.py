"""
Streamlit app for an AI Chat Assistant that interacts with a FastAPI backend
hosted on Google Cloud Run.
"""

import streamlit as st
import requests

HOST = (
    "https://wissalbenothmen-tp3-api-1021317796643.europe-west1.run.app/answer"
)

st.title("AI Chat Assistant")

with st.sidebar:
    temperature = st.slider(
        "Select response creativity (temperature)", 0.0, 1.0, 0.7
    )
    language = st.selectbox(
        "Select answer language", ["English", "French", "Arabic"]
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question?"}
    ]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

if user_question := st.chat_input("What is your question?"):
    st.session_state["messages"].append(
        {"role": "user", "content": user_question}
    )
    st.chat_message("user").write(user_question)

    payload = {
        "question": user_question,
        "temperature": temperature,
        "language": language,
    }

    try:
        response = requests.post(HOST, json=payload, timeout=20)
        if response.status_code == 200:
            assistant_reply = response.json().get(
                "message", "No response from API"
            )
            st.session_state["messages"].append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.chat_message("assistant").write(assistant_reply)
        else:
            st.chat_message("assistant").write(
                "Error: Unable to get a response from the API"
            )
    except requests.ConnectionError as e:
        st.chat_message("assistant").write(f"Connection error: {e}")
# [missing-final-newline]
