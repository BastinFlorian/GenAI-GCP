import streamlit as st

# Sidebar for options
st.sidebar.title("Options")
language = st.sidebar.radio("Select Language:", ["English", "French"])

# Main title
st.title("Hello, Streamlit!")

# Display input fields
if language == "English":
    gender_label = "Select Gender:"
    name_label = "What is your name?"
    submit_label = "Submit"
    greeting_man = "Hello Mr."
    greeting_woman = "Hello Mrs."
else:
    gender_label = "Sélectionnez le genre :"
    name_label = "Quel est votre nom ?"
    submit_label = "Soumettre"
    greeting_man = "Bonjour monsieur"
    greeting_woman = "Bonjour madame"

gender = st.selectbox(gender_label, ["Man" if language == "English" else "Homme", 
                                     "Woman" if language == "English" else "Femme"])
name = st.text_input(name_label)

# Submit button
if st.button(submit_label):
    if name:
        if gender in ["Man", "Homme"]:
            st.success(f"{greeting_man} {name}")
        else:
            st.success(f"{greeting_woman} {name}")
    else:
        st.warning("Please enter your name!" if language == "English" else "Veuillez entrer votre nom !")
