"""Streamlit app"""
import streamlit as st
import requests

# Définir l'URL de l'API FastAPI (en local)
#HOST = "http://localhost:8080/answer"  
HOST = "https://kh-api-1021317796643.europe-west1.run.app/answer"

# Interface utilisateur avec Streamlit
st.title('Hello, Streamlit!')

# Champs de saisie utilisateur
name = st.text_input("Entrez votre nom :")
genre = st.text_input("Entrez votre genre  :")
language = st.text_input("Entrez votre langue :")

# Soumission des données
if st.button("Envoyer"):
    try:
        # Préparer les données pour l'API
        user_data = {
            "name": name,
            "genre": genre,
            "language": language
        }

        # Appeler l'API FastAPI via POST
        response = requests.post(
            HOST,
            json=user_data,
            timeout=20
        )

        # Vérifier la réponse de l'API
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Erreur: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API: {e}")