"""Streamlit app"""

import streamlit as st

# Set the title
st.title('Hello, Streamlit!')

# Create buttons for Language selection
language = st.radio('Select Language:', ('English', 'French'))

# Create buttons for Gender selection
gender = st.radio('Select Gender:', ('Man', 'Woman'))

# Adapt the input sentence to ask for the name of the person
name = st.text_input('What is your name?')

# Logic for output sentence based on language and gender
if name:
    if language == 'English' and gender == 'Man':
        st.write(f"Hello Mr. {name}")
    elif language == 'English' and gender == 'Woman':
        st.write(f"Hello Mrs. {name}")
    elif language == 'French' and gender == 'Man':
        st.write(f"Bonjour monsieur {name}")
    elif language == 'French' and gender == 'Woman':
        st.write(f"Bonjour madame {name}")
