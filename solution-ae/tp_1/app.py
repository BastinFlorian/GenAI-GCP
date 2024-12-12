"""Streamlit app"""

import streamlit as st


st.title('Hello !')

language = st.sidebar.selectbox("Choose your language:", ('English', 'French'))

gender = st.sidebar.selectbox("Choose your gender:", ('Man', 'Woman'))


name = st.text_input("Please enter your name:")


if name:
    
    if language == "English" and gender == "Man":
        st.write(f"Hello Mr. {name}")
    elif language == "English" and gender == "Woman":
        st.write(f"Hello Ms. {name}")
    elif language == "French" and gender == "Man":
        st.write(f"Bonjour monsieur {name}")
    elif language == "French" and gender == "Woman":
        st.write(f"Bonjour madame {name}")