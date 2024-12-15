"""Streamlit app"""
import streamlit as st
import requests

# URL de l'API
#API_URL = "http://127.0.0.1:8080"
API_URL = "https://emchatapi-1021317796643.europe-west1.run.app"

st.title("AI Story Generator")

# Barre latérale pour les paramètres avancés
with st.sidebar:
    st.header("Settings")
    temperature = st.slider(
        "Creativity Level (Temperature)", min_value=0.0, max_value=1.0, value=0.5
    )
    language = st.selectbox("Language", ["English", "French", "Arabic"])

# Initialiser l'état de session pour stocker les messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your theme?"}  # Message initial du chatbot
    ]

# Champ d'entrée pour la question de l'utilisateur
user_input = st.chat_input("Enter your story theme here...")  # Champ d'entrée stylé pour l'utilisateur

# Ajouter la question de l'utilisateur et obtenir la réponse
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})  # Ajouter le message utilisateur

    # Préparer le payload pour l'API
    payload = {
        "question": user_input,
        "temperature": temperature,
        "language": language,
    }

    # Appeler l'API pour générer une réponse
    try:
        response = requests.post(f"{API_URL}/generate-story", json=payload)
        response.raise_for_status()
        api_response = response.json()

        # Ajouter la réponse du chatbot
        if "story" in api_response:
            st.session_state["messages"].append(
                {"role": "assistant", "content": api_response["story"]}
            )
        else:
            st.error("Unexpected API response format.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {e}")

# Afficher les messages sous forme de conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):  # Utiliser des messages stylisés
        st.write(msg["content"])
