import streamlit as st
import pandas as pd
import requests

# Function to get ELO data from the API
def get_elo_data():
    response = requests.get('http://0.0.0.0:8181/get_model_ranking')
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to fetch data from API')
        return None


# Fetch data from the API
elo_data = get_elo_data()

if elo_data:
    # Create a DataFrame
    df = pd.DataFrame(elo_data)

    # Streamlit interface
    st.title('LLM Ranking Table')

    st.table(df)
