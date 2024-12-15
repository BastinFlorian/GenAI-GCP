"""Streamlit app"""
import streamlit as st

st.title("Hello World Streamlit App")
st.write("Welcome to your first Streamlit app!")

language = st.sidebar.selectbox("Choisir la langue", ["Anglais", "Francais"])

gender = st.sidebar.selectbox("Choisir le genre", ["homme", "femme"])

name = st.text_input("Entrer le nom de la personne:") 

greeting = ""

if name:
    if language == "Anglais":
        if gender == "homme":
            greeting = f"Hello M. {name}"
        else:  
            greeting = f"Hello Mme. {name}"
    else:  
        if gender == "homme":
            greeting = f"Bonjour Monsieur {name}"
        else:  
            greeting = f"Bonjour Madame {name}"

if greeting:
    st.write(greeting)