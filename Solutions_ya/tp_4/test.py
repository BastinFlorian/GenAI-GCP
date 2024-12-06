import streamlit as st
import requests
from pydantic import BaseModel

# API URL for your FastAPI app
API_URL = "http://127.0.0.1:8181/answer"

# Define UserInput schema for consistency
class UserInput(BaseModel):
    question: str
    temperature: float
    language: str
    similarity_threshold: float

def fetch_answer(user_input: UserInput):
    response = requests.post(API_URL, json=user_input.dict())
    return response.json()

def main():
    st.title("Generative AI Assistant")
    
    # User input form
    with st.form(key='user_input_form'):
        question = st.text_input("Your question:")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        language = st.selectbox("Language", ["English", "French", "Spanish"])
        similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.65)
        
        submit_button = st.form_submit_button(label="Get Answer")
        
        if submit_button:
            # Prepare the input for the API call
            user_input = UserInput(
                question=question,
                temperature=temperature,
                language=language,
                similarity_threshold=similarity_threshold
            )
            
            # Call the FastAPI backend to get the response
            with st.spinner("Fetching answer..."):
                answer = fetch_answer(user_input)
            
            # Display the answer or error
            if answer.get("status") == "Processing":
                st.success("Processing, please check back soon.")
            elif "error" in answer:
                st.error(f"Error: {answer['error']}")
            else:
                st.write(answer)

if __name__ == "__main__":
    main()
