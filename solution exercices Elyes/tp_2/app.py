"""Streamlit app"""

#Frontend de l'application utilisant Streamlit.
#Permet aux utilisateurs d'entrer leur nom, leur genre, et leur langue.
#Envoie ces informations au backend FastAPI pour générer un message de salutation.


import streamlit as st
import requests

# Définir l'URL du backend FastAPI
#HOST = "http://fastapi:8282/answer"
HOST = "https://elyesapi-63idnujfwq-ew.a.run.app/answer"

# Dictionnaires pour la traduction des textes
translations = {
    "English": {
        "title": "Hello, Streamlit!",
        "sidebar_title": "Options",
        "language_label": "Select Language:",
        "gender_label": "Select Gender:",
        "name_label": "What is your name?",
        "error_api": "Error: Unable to connect to the API.",
        "error_connection": "Connection error with the API:",
        "submit_button": "Submit",
        "name_warning": "Please enter your name.",
    },
    "French": {
        "title": "Bonjour, Streamlit!",
        "sidebar_title": "Options",
        "language_label": "Choisir la langue :",
        "gender_label": "Choisir le genre :",
        "name_label": "Quel est votre nom ?",
        "error_api": "Erreur : Impossible de se connecter à l'API.",
        "error_connection": "Erreur de connexion avec l'API :",
        "submit_button": "Soumettre",
        "name_warning": "Veuillez entrer votre nom.",
    },
}

# Initialisation de l'état (session_state)
if "language" not in st.session_state:
    st.session_state.language = "English"
if "gender" not in st.session_state:
    st.session_state.gender = "Man"

# Sélection de la langue dans la barre latérale
st.sidebar.title("Options")
st.session_state.language = st.sidebar.radio(
    "Select Language:", ["English", "French"], index=0 if st.session_state.language == "English" else 1
)

# Traductions dynamiques en fonction de la langue sélectionnée
lang = st.session_state.language
t = translations[lang]

# Interface principale
st.title(t["title"])

# Sélection du genre
st.session_state.gender = st.sidebar.radio(
    t["gender_label"], ["Man", "Woman"] if lang == "English" else ["Homme", "Femme"]
)

# Entrée utilisateur pour le nom
name = st.text_input(t["name_label"])

# Bouton de soumission
if st.button(t["submit_button"]):
    if name:
        # Préparer les données pour l'API
        user_input = {
            "name": name,
            "genre": st.session_state.gender,
            "language": lang,
        }

        # Appel à l'API
        try:
            response = requests.post(HOST, json=user_input, timeout=20)
            if response.status_code == 200:
                # Afficher le message de salutation
                st.success(response.json()["message"])
            else:
                st.error(t["error_api"])
        except requests.exceptions.RequestException as e:
            st.error(f"{t['error_connection']} {e}")
    else:
        st.warning(t["name_warning"])
