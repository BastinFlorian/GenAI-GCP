"""Streamlit app"""

import streamlit as st
import requests

# Define the API URL
# HOST = "http://fastapi-container:8181/answer"
HOST = "https://sk-1021317796643.europe-west1.run.app/answer"

# User interface with Streamlit
st.title("Hello, Streamlit!")

# User input fields
name = st.text_input("Enter your name:")
genre = st.text_input("Enter your genre:")
language = st.text_input("Enter your language:")

# Submit data
if st.button("Send"):
    try:
        # Prepare data for API
        user_data = {"name": name, "genre": genre, "language": language}

        # Call FastAPI via POST
        response = requests.post(HOST, json=user_data, timeout=20)

        # Check API response
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
