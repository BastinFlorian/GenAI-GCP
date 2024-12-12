import streamlit as st

# App title
st.title('Hello, Streamlit!')

# Sidebar selection for language and gender
language = st.sidebar.selectbox('Language', ['English', 'French'])
gender = st.sidebar.selectbox('Gender', ['Man', 'Woman'])

