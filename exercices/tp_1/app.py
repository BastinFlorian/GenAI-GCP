
import streamlit as st

# Title of the app
st.title('Hello, Streamlit!')

# Sidebar for language and gender selection
language = st.sidebar.selectbox("Select Language:", ["English", "French"])
gender = st.sidebar.selectbox("Select Gender:", ["Man", "Woman"])

# Input for the person's name
name = st.text_input("What is your name?")

# Display the appropriate greeting based on input
if name:
    if language == "English" and gender == "Man":
        st.write(f"Hello Mr. {name}")
    elif language == "English" and gender == "Woman":
        st.write(f"Hello Ms. {name}")
    elif language == "French" and gender == "Man":
        st.write(f"Bonjour monsieur {name}")
    elif language == "French" and gender == "Woman":
        st.write(f"Bonjour madame {name}")

