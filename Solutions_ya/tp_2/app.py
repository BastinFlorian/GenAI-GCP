"""Streamlit app"""
import streamlit as st
import requests

# Define the API host URL
HOST = "http://localhost:8181/answer"  # Replace [container_name] with the actual container name or IP

# Streamlit UI elements
st.sidebar.header("Preferences")
language = st.sidebar.selectbox("Choose your language:", ["English", "Francais"])
if language == "English":
    gender_label = "Choose your gender:"
    man_label = "Man"
    woman_label = "Woman"
    name_label = "Please enter your name:"
else:
    gender_label = "Choisissez votre sexe :"
    man_label = "Homme"
    woman_label = "Femme"
    name_label = "Veuillez entrer votre nom :"

gender = st.sidebar.selectbox(gender_label, [man_label, woman_label])
name = st.text_input(name_label)

if name:
    # Send POST request to the API
    try:
        response = requests.post(
            HOST,
            json={"name": name, "genre": gender, "language": language},
            timeout=20
        )
        
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("Error: Unable to get a response from the API")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
