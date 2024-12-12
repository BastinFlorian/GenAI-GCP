import streamlit as st
import requests

# API URL
API_URL = "https://ae-api-1021317796643.europe-west1.run.app/answer"

if "messages" not in st.session_state:
   st.session_state["messages"] = [{"role": "assistant", "content": "Could you suggest a theme for a story?"}]

st.sidebar.header("Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)
language = st.sidebar.selectbox("Language", ["English", "French", "Arabic"])

st.title("Story telling")
for story in st.session_state["messages"]:
   if story["role"] == "user":
      st.chat_message("user").write(story["content"])
   else:
      st.chat_message("assistant").write(story["content"])
if user_input := st.chat_input("Suggest a theme"):
   st.session_state["messages"].append({"role": "user", "content": user_input})
   try:
      response = requests.post(
            API_URL,
            json={"question": user_input, "temperature": temperature, "language": language},
            timeout=10
      )
      if response.status_code == 200:
            api_response = response.json()["message"]
      else:
            api_response = "Error: Unable to process your request."
   except requests.exceptions.RequestException as e:
      api_response = f"Error: {e}"

   st.session_state["messages"].append({"role": "assistant", "content": api_response})
   st.rerun()
