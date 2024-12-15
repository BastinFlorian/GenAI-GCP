import streamlit as st
import requests

#HOST = "http://localhost:8181/answer"
HOST = "https://nby-api-1021317796643.europe-west1.run.app/answer"

st.title('Hello !')

name = st.text_input('Enter your name')
genre = st.text_input('What genre do you prefer?')
language = st.text_input("Preferred language")

if st.button('Submit'):
    if name and genre and language:
        user_data = {
            "name": name,
            "genre": genre,
            "language": language
        }

        try:
            response = requests.post(HOST, json=user_data, timeout=20)
            if response.status_code == 200:
                st.write(response.json()["message"])
            else:
                st.write(f"Error {response.status_code}: Unable to get a response from the API")
        except requests.exceptions.RequestException as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please fill all the fields.")




























