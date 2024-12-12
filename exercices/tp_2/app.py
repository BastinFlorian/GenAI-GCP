"""Streamlit app"""
import streamlit as st
import requests

# Set the host URL for the FastAPI endpoint.
# Replace `localhost` with the container name if running in Docker.
HOST = (
    "https://bilelguembri-api-tp2-1021317796643.europe-west1.run.app"
    "/answer"
)

st.title('Hello, Streamlit!')

# Add input fields for language, gender, and name
language = st.sidebar.selectbox("Language", ["English", "French"])
genre = st.sidebar.selectbox("Gender", ["Man", "Woman"])
name = st.text_input("Enter your name:")

# Send a POST request to FastAPI if the user provides their name
if name:
    # Create the payload matching UserInput model
    payload = {
        "name": name,
        "genre": genre,
        "language": language
    }

    # Send request to the FastAPI endpoint
    response = requests.post(HOST, json=payload, timeout=20)

    # Display the response message or an error
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")
