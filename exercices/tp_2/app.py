# Streamlit app
import streamlit as st
import requests

HOST = "http://fastapi-container:8181/answer"

st.title('Hello, Streamlit!')
name = st.text_input('Enter your name')
genre = st.selectbox('Select your gender', ('male', 'female'))
language = st.selectbox('Select your language', ('English', 'French'))

if st.button("Submit"):
    response = requests.post(
        HOST,
        json={'name': name, 'genre': genre, 'language': language},
        timeout=20
    )
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")