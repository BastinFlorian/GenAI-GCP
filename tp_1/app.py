"""Streamlit app"""
import streamlit as st 


st.title('Hello, Streamlit!')



# Barre latérale pour les choix
st.sidebar.header("Settings")

# Sélection de la langue
language = st.sidebar.selectbox("Language", ["English", "French"])

# Sélection du genre
gender = st.sidebar.selectbox("Gender", ["Man", "Woman"])

# Demande du nom de la personne
name = st.text_input("What is your name?")

# Message personnalisé en fonction de la langue et du genre
if name:
    if language == "English" and gender == "Man":
        st.write(f"Hello Mr. {name}")
    elif language == "French" and gender == "Woman":
        st.write(f"Bonjour madame {name}")
    elif language == "English" and gender == "Woman":
        st.write(f"Hello Mrs. {name}")
    elif language == "French" and gender == "Man":
        st.write(f"Bonjour monsieur {name}")

