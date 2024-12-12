"""Streamlit app"""
import streamlit as st
import requests

HOST = "http://127.0.0.1:8000/answer"

language = st.sidebar.selectbox("Choose your language:", ('English', 'French'))

gender = st.sidebar.selectbox("Choose your gender:", ('Man', 'Woman'))


name = st.text_input("Please enter your name:")


if name:
    
    if language == "English" and gender == "Man":
        st.write(f"Hello Mr. {name}")
    elif language == "English" and gender == "Woman":
        st.write(f"Hello Ms. {name}")
    elif language == "French" and gender == "Man":
        st.write(f"Bonjour monsieur {name}")
    elif language == "French" and gender == "Woman":
        st.write(f"Bonjour madame {name}")
    payload = {
        "name": name,
        "genre": gender,
        "language": language
    }

    response = requests.post(
            HOST,
            json=payload,
            timeout=20
        )

    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")
