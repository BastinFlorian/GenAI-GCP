"""Streamlit app"""
import streamlit as st
import requests


HOST = "http://localhost:8181/answer"

st.sidebar.write("Select Language:")
language = st.sidebar.selectbox("Language", ["English", "French"])

# Create a sidebar for gender selection
st.sidebar.write("Select Gender:")
gender = st.sidebar.selectbox("Gender", ["Man", "Woman"])

st.title('Hello, Streamlit!')
message = st.text_input('Say something')


if message:
    
    response = requests.post(
        HOST,
        
        json={"name": message, "genre": gender, "language": language},
        timeout=20
    )
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")
