"""Streamlit app"""
import streamlit as st


st.title('Hello, Streamlit!')
message = st.text_input('Say something')
if message:
    st.write(f'You said: {message}')
language = st.sidebar.selectbox('Language:', ['English', 'French'])
gender = st.sidebar.selectbox('Gender:', ['Man', 'Woman'])

# Input for the name of the person
name = st.text_input('Enter your name')

# Conditional message based on language and gender
if name:
    if language == 'English' and gender == 'Man':
        st.write(f'Hello Mr. {name}')
    elif language == 'English' and gender == 'Woman':
        st.write(f'Hello Mrs. {name}')
    elif language == 'French' and gender == 'Man':
        st.write(f'Bonjour monsieur {name}')
    elif language == 'French' and gender == 'Woman':
        st.write(f'Bonjour madame {name}')

