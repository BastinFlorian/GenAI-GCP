"""Streamlit app"""
import streamlit as st
import requests

# Définir l'URL de l'API FastAPI (en local)
# Par exemple, si vous lancez l'API sur le port 8080 :
#HOST = "http://localhost:8080/answer"  
HOST = "https://khtp3api-1021317796643.europe-west1.run.app/answer"

st.title('Story Telling AI Assistant')

with st.sidebar:
    st.write("Options")
    temperature = st.slider("Select Temperature:", 0.0, 1.0, 0.7, 0.1)
    language = st.selectbox("Select Language:", ["English", "French", "Arabic"])

# Initialiser l'historique
# "messages" : liste de dict { "role": "assistant" ou "user", "content": "..." }
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question ?"}
    ]

# Afficher l'historique des messages
for message in st.session_state["messages"]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Champ d'entrée utilisateur
#if question := st.chat_input("What is your question ?"):
if question := st.chat_input("What is your theme ?"):
    # Ajouter le message utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": question})

    # Préparer les données pour l'API
    user_data = {
        "question": question,
        "temperature": temperature,
        "language": language
    }

    # Appeler l'API FastAPI via POST
    try:
        response = requests.post(HOST, json=user_data, timeout=20)
        if response.status_code == 200:
            # Récupérer la réponse de l'API
            msg = response.json()["message"]
            # Ajouter à l'historique
            st.session_state["messages"].append({"role": "assistant", "content": msg})
            # Afficher le nouveau message assistant
            with st.chat_message("assistant"):
                st.write(msg)
        else:
            st.error(f"Erreur: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API: {e}")
