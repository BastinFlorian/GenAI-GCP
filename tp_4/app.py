# Streamlit App
from typing import Dict, List
import streamlit as st
import requests

HOST = "http://localhost:8181/answer"



st.title("Question Answering Hiba's App")

# Sidebar settings
with st.sidebar:
    # contrôler de la variabilité des réponses générées
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05
    )
    language = st.selectbox('Language', ['English', 'French', 'Arabic'])

# initialisation de l'état de session pour stocker l'historique des messages
if "messages" not in st.session_state:
    # définir un message par défaut de l'assistant pour démarrer la conversation
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    st.chat_message(message["role"], avatar=avatar).write(message["content"])

# User input handling
if question := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user", avatar="🧑‍💻").write(question)

    # Make requests to the FastAPI backend
    response = requests.post(
        f"{HOST}/answer",
        json={
            "question": question,
            "temperature": temperature,
            "language": language
        },
        timeout=30
    )

    documents = requests.post(
        f"{HOST}/get_sources",
        json={
            "question": question,
            "temperature": temperature,
            "language": language
        },
        timeout=30 # Temps d'attente maximal pour la réponse
    )

    # effectue une requête Post vers l'API backend pour obtenir une réponse à la question
    if response.status_code == 200:
        answer = response.json()["message"]
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        st.chat_message("assistant", avatar="🤖").write(answer)
    else:
        # gère les erreurs et affiche un message d'erreur si l'API ne répond pas
        st.write("Error: Unable to get a response from the API")
        st.write(f"The error is: {response.text}")

    # Handle response for source documents
    if documents.status_code == 200:
        # récupère les documents sources en tant que liste de dictionnaires
        sources: List[Dict[str, str]] = documents.json()
        for i, source in enumerate(sources):
            with st.expander(f"Source {i+1}"):
                st.write("Metadata:")
                st.write(source["metadata"])
                st.write("Content:")
                st.write(source["page_content"])
    else:
        st.write("Error: Unable to retrieve source documents")
        st.write(f"The error is: {documents.text}")