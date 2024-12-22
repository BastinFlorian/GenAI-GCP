"""Streamlit app"""

import streamlit as st
import requests

# Définir l'URL de l'API déployée
# HOST = "http://api-container:8181/answer"
HOST = "https://sk-1021317796643.europe-west1.run.app/answer"

# Titre de l'application
st.title("Chatbot Streamlit")

# Ajouter un menu latéral pour choisir la température et la langue
with st.sidebar:
    st.header("Paramètres")
    temperature = st.slider(
        "Choisir la température du modèle", min_value=0.0, max_value=1.0, value=0.5
    )
    language = st.selectbox(
        "Choisir la langue de la réponse", ["French", "English", "Arabic"]
    )

# Initialisation de l'historique des messages si ce n'est pas déjà fait
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question ?"}
    ]

# Affichage de l'historique des messages
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).text(message["content"])

# Capture de la question de l'utilisateur
if question := st.chat_input("What is your question ?"):
    # Ajouter la question de l'utilisateur à l'historique des messages
    st.session_state["messages"].append({"role": "user", "content": question})

    # Appeler l'API pour obtenir la réponse avec un timeout
    try:
        response = requests.post(
            HOST,
            json={
                "question": question,
                "temperature": temperature,
                "language": language,
            },
            timeout=10,  # Add timeout
        )
        response.raise_for_status()  # Raise an error for bad status codes

        # Obtenir la réponse et l'ajouter à l'historique des messages
        answer = response.json().get("answer", "Sorry, I didn't get that.")
    except requests.exceptions.RequestException as e:
        answer = f"Error communicating with the API: {e}"

    # Ajouter la réponse du chatbot à l'historique
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Mettre à jour l'affichage du message de l'assistant
    st.chat_message("assistant").text(answer)
