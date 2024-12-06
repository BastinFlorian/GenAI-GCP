import streamlit as st

st.sidebar.header("Preferences")

language = st.sidebar.selectbox("Choose your language:", ['English', 'Francais'])


if language == 'English':
    st.title("Welcome")
    gender_label = "Choose your gender:"
    man_label = "Man"
    woman_label = "Woman"
    name_label = "Please enter your name:"
    submit_button = "Submit"
else:
    st.title("Bienvenue")
    gender_label = "Choisissez votre sexe :"
    man_label = "Homme"
    woman_label = "Femme"
    name_label = "Veuillez entrer votre nom :"
    submit_button = "Soumettre"

gender = st.sidebar.selectbox(gender_label, [man_label, woman_label])

name = st.text_input(name_label)

if name:
    if language == 'English' and gender == man_label:
        st.success(f"Hello Mr. {name}")
    elif language == 'English' and gender == woman_label:
        st.success(f"Hello Ms. {name}")
    elif language == 'Francais' and gender == man_label:
        st.success(f"Bonjour monsieur {name}")
    elif language == 'Francais' and gender == woman_label:
        st.success(f"Bonjour madame {name}")
