import os
from typing import Dict, List
import streamlit as st
import requests

# HOST = "http://0.0.0.0:8181/answer"  # Docker run name of Fast API
#HOST = "http://localhost:8181"
HOST = "https://mi4-1021317796643.europe-west1.run.app/answer"  # Cloud Run

# Titre et en-tête
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🌟 Meriam RAG Assistant 🌟")
st.markdown("Bienvenue dans l'application de Chatbot utilisant le *RAG* (Retrieval Augmented Generation) ! 💬")

# Section pour récupérer les fichiers depuis le backend
if "files_fetched" not in st.session_state:
    st.session_state.files_fetched = False
    st.session_state.files = []

if not st.session_state.files_fetched:
    try:
        response = requests.post(f"{HOST}/get_files_names", timeout=30)
        files = response.json().get("files", [])
        if files:
            st.session_state.files = files
            st.session_state.files_fetched = True
        else:
            st.info("🚫 Aucun fichier trouvé dans le bucket.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Échec de la récupération des fichiers : {e}")

# Barre latérale (Sidebar)
with st.sidebar:
    st.header("⚙️ Paramètres")
    temperature = st.slider(
        "🌡️ Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05
    )
    similarity_threshold = st.slider(
        "🔍 Seuil de Similarité RAG",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05,
        disabled=True,
    )
    language = st.selectbox("🌍 Langue", ["English", "Français", "Arabic"])

    st.subheader("📂 Fichiers Ingérés")
    for file in st.session_state.files[1:]:
        st.write(file[5:])

# Section des messages du Chatbot
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How may I help you?", "sources": []}
    ]

# Affichage des messages dans la fenêtre de chat
for n, message in enumerate(st.session_state.messages):
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    st.chat_message(message["role"], avatar=avatar).write(message["content"])

    # Affichage des sources si présentes
    if "sources" in message and message["sources"]:
        for i, source in enumerate(message["sources"]):
            if source["metadata"]["score"] >= similarity_threshold:
                with st.expander(
                    f"Source {i+1}    -    pertinence: {(source['metadata']['score'])*100:.2f}%"
                ):
                    st.write("🔑 Metadata :")
                    st.write(source["metadata"])
                    st.write("📄 Contenu :")
                    st.write(source["page_content"])

# Entrée de l'utilisateur
if question := st.chat_input("Posez votre question 🤖"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    # Envoi de la requête pour obtenir des documents
    documents = requests.post(
        f"{HOST}/get_sources",
        json={
            "question": question,
            "temperature": temperature,
            "similarity_threshold": similarity_threshold,
            "language": language,
            "documents": [],
            "previous_context": [],
        },
        timeout=30,
    )

    docs = documents.json()

    if not isinstance(docs, list):
        docs = []

    # Envoi de la question pour obtenir la réponse du Chatbot
    response = requests.post(
        f"{HOST}/answer",
        json={
            "question": question,
            "temperature": temperature,
            "similarity_threshold": similarity_threshold,
            "language": language,
            "documents": docs,
            "previous_context": st.session_state["messages"],
        },
        timeout=30,
    )

    if response.status_code == 200:
        answer = response.json()["message"]
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": []}
        )
        st.chat_message("assistant", avatar="🤖").write(answer)
    else:
        st.write("❌ Erreur : Impossible d'obtenir une réponse de l'API (réponse)")
        st.write(f"L'erreur est : {response.text}\nCode de statut : {response.status_code}")

    if documents.status_code == 200:
        sources: List[Dict[str, str]] = documents.json()
        st.session_state.messages[-1][
            "sources"
        ] = sources  # Attacher les sources à la dernière réponse
        for i, source in enumerate(sources):
            if source["metadata"]["score"] >= similarity_threshold:
                with st.expander(
                    f"Source {i+1}    -    pertinence: {(source['metadata']['score'])*100:.2f}%"
                ):
                    st.write("🔑 Metadata :")
                    st.write(source["metadata"])
                    st.write("📄 Contenu :")
                    st.write(source["page_content"])
    else:
        st.write("❌ Erreur : Impossible d'obtenir des sources de l'API (documents)")
        st.write(
            f"L'erreur est : {documents.text}\nCode de statut : {documents.status_code}"
        )
