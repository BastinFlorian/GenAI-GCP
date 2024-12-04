"""Streamlit app"""
import streamlit as st


st.title('Hello!')
message = st.text_input('Say something')
if message:
    st.write(f'You said: {message}')
# Create a sidebar for language selection
st.sidebar.write("Select Language:")
language = st.sidebar.selectbox("Language", ["English", "French"])

# Create a sidebar for gender selection
st.sidebar.write("Select Gender:")
gender = st.sidebar.selectbox("Gender", ["Man", "Woman"])

# Adapt the input sentence to ask for the person's name
if language == 'English':
    name = st.text_input("Please enter your name:")
else:
    name = st.text_input("Veuillez entrer votre nom:")

# Show the greeting message based on the selected options
if st.button("Submit"):
    if language == 'English' and gender == 'Man':
        st.write(f"Hello Mr. {name}")
    elif language == 'English' and gender == 'Woman':
        st.write(f"Hello Ms. {name}")
    elif language == 'French' and gender == 'Man':
        st.write(f"Bonjour monsieur {name}")
    elif language == 'French' and gender == 'Woman':
        st.write(f"Bonjour madame {name}")