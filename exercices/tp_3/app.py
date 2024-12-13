import streamlit as st
import requests

# Remplacer par l'URL de ton API FastAPI déployée
HOST = "https://rm-tp3-api-1021317796643.europe-west1.run.app/answer"  # Utilise l'URL de ton API FastAPI déployée

# Affichage du titre
st.title("Fast-Accurate Story")

# Initialiser la liste des messages si elle n'existe pas encore
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What theme would you like to explore?/Quel thème souhaitez-vous explorer ?"}]

# Paramètres du modèle
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
language = st.sidebar.selectbox("Language / Langue", ["English", "French", "Arabic"])
genre = st.sidebar.selectbox("Genre", ["Adventure", "Fantasy", "Sci-fi"])

# Affichage de l'historique des messages
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).markdown(message["content"])

# Zone de texte pour le thème
if theme := st.chat_input("What theme would you like to explore?/Quel thème souhaitez-vous explorer ?"):
    # Ajoute le thème de l'utilisateur dans la liste des messages
    st.session_state["messages"].append({"role": "user", "content": theme})

    # Affiche immédiatement la question dans l'historique avant d'attendre la réponse
    st.chat_message("user").markdown(theme)
    
    # Appel à l'API FastAPI avec les paramètres appropriés
    payload = {
        "question": theme,  # Remarquez que la variable "question" est utilisée ici, mais le thème est la nouvelle entrée
        "temperature": temperature,
        "language": language,
        "genre": genre
    }

    # Appel API à FastAPI
    response = requests.post(f"{HOST}/answer", json=payload)
    #response = requests.post(f"http://fastapi-chat-container:8080/answer", json=payload)

    if response.status_code == 200:
        # La réponse générée par l'API
        answer = response.json().get("message", "Sorry, I couldn't process your request./Je suis désolé, je ne pourrai pas satisfaire à votre requête.")
        
        # Ajoute la réponse dans les messages
        st.session_state["messages"].append({"role": "assistant", "content": answer})

        # Affiche immédiatement la réponse de l'assistant
        st.chat_message("assistant").markdown(answer)
    else:
        # Si une erreur survient lors de l'appel API
        st.session_state["messages"].append({"role": "assistant", "content": "There was an error with the API."})

        # Affiche immédiatement un message d'erreur
        st.chat_message("assistant").markdown("There was an error with the API.")
