"""Streamlit app"""
import streamlit as st
import requests

# Définir l'URL de l'API FastAPI déployée
HOST = "https://rm-api-1021317796643.europe-west1.run.app/answer"  # Utiliser le nom du conteneur de l'API et le port exposé

st.title('Hello, Streamlit!')
message = st.text_input("What's your name?/Quel est votre nom")

if message:
    # Envoi de la requête POST à l'API
    user_input = {
        "name": message,  # Utilisation de l'input utilisateur comme nom
        "genre": st.sidebar.selectbox("Select Gender", ["Man", "Woman", "Homme", "Femme"]),
        "language": st.sidebar.selectbox("Select Language", ["English", "Français"])
    }
    
    # Envoi de la requête POST
    response = requests.post(
        HOST,
        json=user_input,  # Envoi des données sous forme de JSON
        timeout=20
    )

    if response.status_code == 200:
        st.write(response.json()["message"])  # Affichage du message retourné par l'API
    else:
        st.write("Error: Unable to get a response from the API")

