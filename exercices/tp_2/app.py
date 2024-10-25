import streamlit as st
import requests

#HOST = "http://fastapi-container:8181/answer"
HOST = "https://mehyar-fastapi-1021317796643.europe-west1.run.app/answer"


# Streamlit app setup
st.title('Hello!')
st.write("Enter your details to receive a personalized message.")

# Input fields
name = st.text_input('Name:')
genre = st.selectbox('Genre:', ['male', 'female'])  
language = st.text_input('Preferred Language:')

# Submit buttonw
if st.button('Submit'):
    if name and genre and language:
        # Prepare the JSON payload
        payload = {
            "name": name,
            "genre": genre,
            "language": language
        }

        #  POST to FastAPI
        try:
            response = requests.post(HOST, json=payload, timeout=20)

            if response.status_code == 200:
                # Display the message from the FastAPI response
                st.write(response.json()["message"])
            else:
                st.write(f"Error: {response.status_code} - Unable to get a response from the API")
        
        except requests.exceptions.RequestException as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please fill in all the fields.")
