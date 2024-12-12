"""
This Streamlit app displays a personalized greeting based on
the user's name, selected language, and gender.
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
    if language == "English":
        if gender == "Man":
            st.write(f"Hello Mr. {name}")
        elif gender == "Woman":
            st.write(f"Hello Ms. {name}")
    elif language == "French":
        if gender == "Man":
            st.write(f"Bonjour monsieur {name}")
        elif gender == "Woman":
            st.write(f"Bonjour madame {name}")
else:
    st.write("Please enter your name.")
# [missing-final-newline]
