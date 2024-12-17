import streamlit as st
import requests

# URL de l'API FastAPI hébergée
#HOST = "http://localhost:8181/answer"
HOST = "https://doniaapi-1021317796643.europe-west1.run.app/answer"

# Sidebar pour sélectionner la langue
st.sidebar.title("Options")
language = st.sidebar.radio("Select Language:", ["English", "French"])

# Titre principal
st.title("Hello, Streamlit!")

# Étiquettes dynamiques selon la langue sélectionnée
if language == "English":
    gender_label = "Select Gender:"
    name_label = "What is your name?"
    submit_label = "Submit"
else:
    gender_label = "Sélectionnez le genre :"
    name_label = "Quel est votre nom ?"
    submit_label = "Soumettre"

# Entrées utilisateur
gender = st.selectbox(
    gender_label, 
    ["Man" if language == "English" else "Homme", "Woman" if language == "English" else "Femme"]
)
name = st.text_input(name_label)

# Soumission des données
if st.button(submit_label):
    if name:
        # Envoyer les données à l'API
        payload = {"name": name, "genre": gender, "language": language}
        try:
            response = requests.post(HOST, json=payload)  # Utiliser HOST ici
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error("Error: Unable to process the request.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your name!" if language == "English" else "Veuillez entrer votre nom !")
