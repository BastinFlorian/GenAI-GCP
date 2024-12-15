import streamlit as st
import requests

# Définir l'URL de l'API FastAPI
HOST = "https://fb-1021317796643.europe-west1.run.app/answer"
#HOST = "http://localhost:8181"

st.title("Choco Bot Interface")

# Configuration dans la barre latérale
with st.sidebar:
    temperature = st.slider("Choose the model's temperature:", min_value=0.0, max_value=1.0, value=0.5)
    language = st.selectbox("Choose the story language:", options=["English", "French", "Arabic"])

# Initialiser l'historique des messages si non présent
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! What is your theme?"}
    ]

# Afficher chaque message de l'historique
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Gestion de la saisie du thème
if theme := st.chat_input("What is your theme?"):
    # Ajouter le thème saisi par l'utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": theme})

    # Afficher immédiatement le thème saisi par l'utilisateur
    st.chat_message("user").markdown(theme)

    # Envoyer le thème à l'API
    try:
        response = requests.post(
            f"{HOST}/generate_story",  # Utiliser une nouvelle route pour générer une histoire
            json={
                "theme": theme,  # Le thème saisi par l'utilisateur
                "temperature": temperature,
                "language": language
            },
            timeout=20  # Timeout pour éviter des attentes infinies
        )

        # Vérifier si la réponse de l'API est réussie
        if response.status_code == 200:
            try:
                # Essayer de récupérer la réponse JSON
                json_response = response.json()

                # Vérifier si la réponse de l'API contient la clé "story"
                if json_response and "story" in json_response:
                    story = json_response.get("story", "No valid response")
                else:
                    story = "API response is empty or malformed."

            except ValueError as e:
                story = f"Error parsing response: {str(e)}"
        else:
            story = f"Error: {response.status_code}. {response.text}"

    except requests.exceptions.RequestException as e:
        story = f"An error occurred while communicating with the API: {e}"

    # Ajouter l'histoire générée par l'API à l'historique
    st.session_state["messages"].append({"role": "assistant", "content": story})

    # Afficher l'histoire générée
    st.chat_message("assistant").markdown(story)
