import streamlit as st
import requests


# API URL
API_URL = "https://ya-api-1021317796643.europe-west1.run.app/answer"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Could you propose a theme for a story?"}]

# Sidebar options
st.sidebar.header("Preferences")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)
language = st.sidebar.selectbox("Language", ["English", "French", "Arabic"])


# Chat UI
st.title("Hello, Streamlit!")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
#Une bataille de 3 robots dans la galaxie à cause des humains
# User input
if user_input := st.chat_input("Ask a question:"):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call the API
    try:
        response = requests.post(
            API_URL,
            json={"question": user_input, "temperature": temperature, "language": language},
            timeout=10
        )
        if response.status_code == 200:
            api_response = response.json()["message"]
        else:
            api_response = "Error: Unable to process your request."
    except requests.exceptions.RequestException as e:
        api_response = f"Error: {e}"

    # Add assistant message to history
    st.session_state["messages"].append({"role": "assistant", "content": api_response})
    st.rerun()
