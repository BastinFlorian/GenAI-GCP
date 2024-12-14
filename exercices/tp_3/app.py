import streamlit as st
import requests

# Initialize Streamlit app
st.title("Chatbot Interface")

# Sidebar for settings
with st.sidebar:
    temperature = st.slider("Select Temperature", 0.0, 1.0, 0.5)
    language = st.selectbox("Select Response Language", ["English", "French", "Arabic"])

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display conversation history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for user questions
if user_input := st.chat_input("Type your question:"):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Prepare API request data
    data = {"question": user_input, "temperature": temperature, "language": language}

    # Call FastAPI backend
    try:
        response = requests.post("http://fastapi-container:8181/answer", json=data)
        if response.status_code == 200:
            answer = response.json().get("message", "No response")
        else:
            answer = f"Error: {response.status_code}"

    except Exception as e:
        answer = f"Error: {e}"

    # Add assistant's response to history
    st.session_state["messages"].append({"role": "assistant", "content": answer})
