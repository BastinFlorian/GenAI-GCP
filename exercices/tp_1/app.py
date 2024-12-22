"""Streamlit app"""

import streamlit as st


st.title("Hello, Streamlit!")
message = st.text_input("Say something")
if message:
    st.write(f"You said: {message}")
