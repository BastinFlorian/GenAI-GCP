"""Streamlit app"""
import streamlit as st
import requests

HOST = "http://localhost:8181/answer"  # L'URL de ton API locale

st.title('Gemini-like Chatbot Interface')

# Ajouter la barre latérale pour les options
with st.sidebar:
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    language = st.selectbox("Select Language", ["English", "French", "Arabic"])

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question?"}
    ]

# Affichage de la conversation
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).markdown(message["content"])

# Capture de la question de l'utilisateur
if question := st.chat_input("What is your question?"):
    st.session_state["messages"].append({"role": "user", "content": question})
    
    # Envoi de la requête à l'API
    response = requests.post(
        HOST,
        json={"question": question, "temperature": temperature, "language": language},
    )
    
    # Affichage de la réponse
    if response.status_code == 200:
        answer = response.json().get("message")
        st.session_state["messages"].append({"role": "assistant", "content": answer})
    else:
        st.session_state["messages"].append({"role": "assistant", "content": "Sorry, I couldn't process your request."})

