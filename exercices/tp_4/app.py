"""Streamlit app"""
from typing import Dict, List
import streamlit as st
import requests

# Définir l'URL de l'API (à ajuster selon l'environnement de déploiement)
HOST = "http://localhost:8181"  # Local host
# HOST = "https://fb-api-1021317796643.europe-west1.run.app"  # Cloud Run

st.title('Hello, Streamlit!')

# Paramètres dans la barre latérale
with st.sidebar:
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    language = st.selectbox('language', ['English', 'Francais', 'Arabic'])

# Stocker les messages dans l'état de session
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question?"}
    ]

for message in st.session_state.messages:
    AVATAR = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    st.chat_message(message["role"], avatar=AVATAR).write(message["content"])

if question := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    response = requests.post(
        f"{HOST}/answer",
        json={
            "question": question,
            "temperature": temperature,
            "language": language
        },
        timeout=20
    )

    documents = requests.post(
    f"{HOST}/get_sources",  # Correct endpoint
    json={
        "question": question,
        "temperature": temperature,
        "language": language
    },
    timeout=20
)


    # Traiter la réponse principale
    if response.status_code == 200:
        answer = response.json().get("message", "No answer provided.")
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant", avatar="🤖").write(answer)
    else:
        st.write("Error: Unable to get a response from the API")
        st.write(f"The error is: {response.text}")

    # Afficher les documents sources si disponibles
    if documents.status_code == 200:
        sources: List[Dict[str, str]] = documents.json()
        for i, source in enumerate(sources):
            with st.expander(f"Source {i+1}"):
                st.write("Metadata:")
                st.write(source["metadata"])
                st.write("Content:")
                st.write(source["page_content"])
    else:
        st.write("Error: Unable to get sources from the API")
        st.write(f"The error is: {documents.text}")
