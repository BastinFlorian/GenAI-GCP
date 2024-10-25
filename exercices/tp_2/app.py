"""Streamlit app"""

import streamlit as st
import requests

HOST = "https://malekmak-api-1021317796643.europe-west1.run.app/answer"

st.title("Hello, Streamlit!")

st.sidebar.header("Preferences")
language = st.sidebar.selectbox("Select Preferred Language", ("English", "Français"))
if language == "English":
    gender = st.sidebar.selectbox("Select Gender", ("Man", "Woman"))
elif language == "Français":
    gender = st.sidebar.selectbox("Choisir Genre", ("Homme", "Femme"))
else:
    gender = st.sidebar.selectbox("Select Gender", ("Man", "Woman"))

message = st.text_input("Please enter your name")
if message:
    response = requests.post(
        HOST, json={"name": message, "genre": gender, "language": language}, timeout=20
    )
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")
