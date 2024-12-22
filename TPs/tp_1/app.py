"""Streamlit app"""

import streamlit as st


st.title("Hello, Streamlit!")
message = st.text_input("Say something")
if message:
    st.write(f"You said: {message}")

# Language selection
language = st.radio("Select Language:", ("English", "French"))

# Gender selection
gender = st.radio("Select Gender:", ("Man", "Woman"))

# Input for name
name = st.text_input("Enter your name:")

# Output based on selections
if st.button("Greet"):
    if language == "English":
        if gender == "Man":
            st.write(f"Hello Mr. {name}")
        else:
            st.write(f"Hello Ms. {name}")
    else:  # French
        if gender == "Man":
            st.write(f"Bonjour Monsieur {name}")
        else:
            st.write(f"Bonjour Madame {name}")
