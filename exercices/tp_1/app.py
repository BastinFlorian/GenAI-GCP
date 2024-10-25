import streamlit as st

st.sidebar.title('Settings')
language = st.sidebar.selectbox('Language', ['English', 'French'])
gender = st.sidebar.selectbox('Gender', ['Man', 'Woman'])

name = st.text_input("What's your name?")

if name:
    if language == 'English' and gender == 'Man':
        st.write(f'Hello Mr. {name}')
    elif language == 'English' and gender == 'Woman':

        st.write(f'Hello Ms. {name}')
    elif language == 'French' and gender == 'Man':
        st.write(f'Bonjour monsieur {name}')
    elif language == 'French' and gender == 'Woman':
        st.write(f'Bonjour madame {name}')
