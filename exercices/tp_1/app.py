"""Streamlit app"""
import streamlit as st


st.title('Hello, Streamlit!')


st.sidebar.header("Preferences")
language = st.sidebar.selectbox("Select Prefered Language", ("English", "French"))
gender = st.sidebar.selectbox("Select Gender", ("Man", "Woman"))


message = st.text_input('Please enter your name')
if message:
    if language == "English":
        if gender == "Man":
            st.write(f'Hello Mr. {message}')
    if language == "English":
        if gender == "Woman":
            st.write(f'Hello Mrs. {message}')
    if language == "French":
        if gender == "Man":
            st.write(f'Bonjour Mr. {message}')
    if language == "French":
        if gender == "Woman":
            st.write(f'Bonjour Mme. {message}')

