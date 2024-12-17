import streamlit as st
import requests

# Hôte local pour l'API
HOST = " https://dtapi3-1021317796643.europe-west1.run.app/answer"

st.title("Hello, Streamlit!")

st.sidebar.header("Preferences")

temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1
)

language = st.sidebar.selectbox("Language", ("English", "Français", "عربي"))

prompt_message = {
    "English": "Enter a theme ...",
    "Français": "Saisir un thème ...",
    "عربي": "أدخل موضوعًا",
}
error_message = {
    "English": "Error: Unable to get a response.",
    "Français": "Erreur : Impossible d'obtenir une réponse.",
    "عربي": "خطأ: غير قادر على الحصول على رد",
}

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! tell me a theme",
        }
    ]


for message in st.session_state["messages"]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])

if prompt := st.chat_input(prompt_message[language]):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    try:
        response = requests.post(
            HOST,
            json={
                "prompt": prompt,
                "temperature": temperature,
                "language": language,
            },
            timeout=20,
        )
        if response.ok:
            st.session_state["messages"].append(
                {"role": "assistant", "content": response.json()["message"]}
            )
            with st.chat_message("assistant"):
                st.write(response.json()["message"])
        else:
            st.session_state["messages"].append(
                {"role": "assistant", "content": error_message[language]}
            )
            with st.chat_message("assistant"):
                st.write(error_message[language])
    except requests.exceptions.RequestException as e:
        st.session_state["messages"].append(
            {"role": "assistant", "content": error_message[language]}
        )
        with st.chat_message("assistant"):
            st.write(error_message[language])
