import requests
import streamlit as st

# Streamlit app title
st.title("Hello, Streamlit!")

# Form elements
name = st.text_input("Enter your name")
genre = st.selectbox("Select gender", ["female", "male", "other"])
language = st.selectbox("Select language", ["English", "French", "Spanish"])

# Submit button
if st.button("Submit"):
    # Prepare data to send in the POST request
    data = {"name": name, "genre": genre, "language": language}
    
    # Use the FastAPI Cloud Run URL
    response = requests.post(
        "https://fastapi-service-1021317796643.europe-west1.run.app/answer",  # Updated to Cloud Run URL
        json=data  # Send data as JSON
    )
    
    # Handle response from FastAPI server
    if response.status_code == 200:
        st.write(response.json()["message"])  # Display response message
    else:
        st.write("Error:", response.status_code)
