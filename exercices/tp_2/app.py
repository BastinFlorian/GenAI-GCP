"""Streamlit app"""
import streamlit as st
import requests

# TODO
# HOST = "http://[container_name]:[host]/answer"

st.title('Hello, Streamlit!')
message = st.text_input('Say something')
if message:
    # TODO
    response = requests.post(
        HOST,
        ...
        json=...,
        timeout=20
    )
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.write("Error: Unable to get a response from the API")
