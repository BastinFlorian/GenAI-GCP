"""Streamlit app"""
import streamlit as st
import requests

HOST =  # TODO

st.title('Hello, Streamlit!')


with st.sidebar:
   # TODO

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What is your question ?"}]


if question := st.chat_input("What is your question ?"):
   # TODO
