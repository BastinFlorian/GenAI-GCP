"""
This module displays a personalized greeting using Streamlit.
"""
import streamlit as st

st.title("Hello, Streamlit!")

# Add language and gender selection in the sidebar
language = st.sidebar.selectbox("Language", ["English", "French"])
gender = st.sidebar.selectbox("Gender", ["Man", "Woman"])

# Get the user's name
name = st.text_input("Enter your name:")

# Display a personalized greeting based on language and gender
if name:
    if language == "English" and gender == "Man":
        st.write(f"Hello Mr. {name}")
    elif language == "French" and gender == "Woman":
        st.write(f"Bonjour madame {name}")
    elif language == "English" and gender == "Woman":
        st.write(f"Hello Ms. {name}")
    elif language == "French" and gender == "Man":
        st.write(f"Bonjour monsieur {name}")
    else:
        st.write(f"Hello {name}")  # default
