import streamlit as st

st.title('Hello !')

message = st.text_input('Say something')
if message:
    st.write(f'You said: {message}')


language = st.sidebar.selectbox('Choose language', ['English', 'French'])
gender = st.sidebar.selectbox('Choose gender', ['Man', 'Woman'])
name = st.text_input('What is your name?')

if name:
    if language == 'English' and gender == 'Man':
        st.write(f'Hello Mr. {name}')
    elif language == 'French' and gender == 'Woman':
        st.write(f'Bonjour Madame {name}')
    elif language == 'English' and gender == 'Woman':
        st.write(f'Hello Ms. {name}')
    elif language == 'French' and gender == 'Man':
        st.write(f'Bonjour Monsieur {name}')
