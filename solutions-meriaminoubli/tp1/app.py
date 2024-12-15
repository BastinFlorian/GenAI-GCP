"""Streamlit app"""
import streamlit as st

HOST = "https://fb-1021317796643.europe-west1.run.app/answer

st.title('Greeting App')

language = st.sidebar.selectbox('Select Language:', ['English', 'French'])

gender = st.sidebar.selectbox('Select Gender:', ['Man', 'Woman'])

name = st.text_input('Please enter your name:')

greeting_message = ""

if name:
    if language == 'English' and gender == 'Man':
        greeting_message = f"Hello Mr. {name}"
    elif language == 'English' and gender == 'Woman':
        greeting_message = f"Hello Ms. {name}"
    elif language == 'French' and gender == 'Man':
        greeting_message = f"Bonjour monsieur {name}"
    elif language == 'French' and gender == 'Woman':
        greeting_message = f"Bonjour madame {name}"

if greeting_message:
    st.write(greeting_message)

