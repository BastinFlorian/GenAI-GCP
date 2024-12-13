"""Streamlit app"""
import streamlit as st

# Titre de l'application
st.title('Hello, Streamlit!')

# Barre latérale pour sélectionner la langue
language = st.sidebar.selectbox("Language/Langue", ["English", "Français"])

# Barre latérale pour sélectionner le genre
gender = st.sidebar.selectbox("Gender/Genre", ["Man", "Homme", "Woman", "Femme"])

# Adaptation du message d'entrée pour demander le nom
name = st.text_input("What's your name?/Quel est votre nom")

# Adaptation de l'affichage en fonction de la langue et du genre
if name:
    if language == "English":
        if (gender == "Man" or gender == "Homme"):
            st.write(f"Hello Mr. {name}")
        elif (gender == "Woman" or gender == "Femme"):
            st.write(f"Hello Ms. {name}")
    elif language == "Français":
        if (gender == "Man" or gender == "Homme"):
            st.write(f"Bonjour Monsieur {name}")
        elif (gender == "Woman" or gender == "Femme"):
            st.write(f"Bonjour Madame {name}")
