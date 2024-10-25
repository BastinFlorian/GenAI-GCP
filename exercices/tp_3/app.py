import streamlit as st
import requests

HOST = "http://localhost:8181/answer"

st.title('Dear User!')

# Sidebar for user settings
with st.sidebar:
    temperature = st.slider("Select Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
    language = st.selectbox("Select Language", options=["English", "French", "Arabic"])

# Initialize messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your Topic?"}
    ]

# Display all chat messages
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).markdown(message["content"])

# Input for user question
if question := st.chat_input("What is your question?"):
    # Append user's question to messages
    st.session_state["messages"].append({"role": "user", "content": question})

    # Create a placeholder for the assistant's response
    placeholder = st.chat_message("assistant")
    placeholder.markdown("Thinking...")

    # Make a request to the backend API
    try:
        response = requests.post(f"{HOST}", json={
            "question": question,
            "temperature": temperature,
            "language": language
        }, timeout=20)

        # Check if the response was successful
        if response.status_code == 200:
            answer = response.json().get("message")
            # Update the placeholder with the actual answer
            placeholder.markdown(answer)
            # Append assistant's response to messages
            st.session_state["messages"].append({"role": "assistant", "content": answer})
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            placeholder.markdown(error_message)
            st.session_state["messages"].append({"role": "assistant", "content": error_message})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        placeholder.markdown(error_message)
        st.session_state["messages"].append({"role": "assistant", "content": error_message})

    # Display updated messages after the API call
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).markdown(message["content"])
