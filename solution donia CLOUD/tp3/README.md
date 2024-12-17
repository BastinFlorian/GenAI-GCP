 uvicorn api:app --host 127.0.0.1 --port 8083

## 3. Create a Gemini-like Interface

The goal of this session is to create a chatbot-like interface that will be able to answer the user's questions.

### 3.1 Create the Streamlit App

Edit the `app.py` file to have the following features:
- `st.chat_message` to display the conversation (documentation [here](https://docs.streamlit.io/develop/api-reference/chat/st.chat_message))
- An option for the user to choose the temperature of the model
- An option for the user to select the answer language ("French", "English", "Arabic")
- Keep the history of the conversation in a list and display it in the chat messages

### 3.2 Create the API Logic

Edit the `api.py` file to:
- Receive in an `/answer` endpoint the user's question, the temperature, and the language
- Return the question, language, and temperature in the response as a sentence: "The user asked the question: `<question>` in `<language>` with a temperature of `<temperature>`"

### 3.3 Test Locally the Streamlit App and the API
- Use TP 2 to test the app and the API locally.

Goal:

![TP 3.1](../../docs/tp_3_1.png)

### 3.4 Edit the `api.py` File to Use a Gemini Model Using LangChain Accelerator
- Edit the `.env` file with the `GOOGLE_API_KEY` variables provided by the instructor
- Follow this tutorial [here](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)
- Install the requirements in the `requirements.txt` file
- Test the Streamlit app by adjusting the temperature and the language

Goal:

![TP 3.2](../../docs/tp_3_2.png)

### 3.5 Create a Short Story Generator

- Edit the prompt to generate a short story about a user-input theme
- Edit the `app.py` to ask for a theme instead of a question
- Leave the `UserInput` class variables unchanged

Goal:

![TP 3.3](../../docs/tp_3_3.png)

### 3.6 Protect Our Environment Variable

### 3.7 Deploy Your Story Generator on Cloud Run
- Deploy the FastAPI app
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _api
# Florian Bastin -> <my-docker-image-name>fb_api
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile_api .

# Be careful, the default port is 8080 for Cloud Run.
# If you have an error message, edit the default Cloud Run port on the interface or in the command line
gcloud run deploy <my-app-name> \
    --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-name>:latest \
    --platform=managed \
    --region=<my-region> \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=[INSERT_GOOGLE_API_KEY] \
    --port 8181

# Note that a SECRET KEY like this should be provided by GOOGLE SECRET MANAGER for more safety.
# For simplicity, we will use the env variable here.
```

- Change the HOST in your `app.py` to the URL of the FastAPI
Example: `HOST = "https://fb-1021317796643.europe-west1.run.app/answer"`

- Deploy the Streamlit app
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _streamlit
# Florian Bastin -> <my-docker-image-name>fb_streamlit
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile .

gcloud run deploy <initials>-streamlit \
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<initials>-streamlit:latest \
    --platform=managed \
    --region=europe-west1 \
    --allow-unauthenticated \
    --port 8080
```
Goal:

![TP 3.4](../../docs/tp_3_4.png)



gcloud config set account doniatekaya04@gmail.com
gcloud config set project dauphine-437611

gcloud projects describe dauphine-437611



------------------------------

docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dtapi3:latest -f Dockerfile_api .

gcloud run deploy dtapi3 `   
>>     --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dtapi3:latest ` 
>>     --platform=managed `
>>     --region=europe-west1 `
>>     --allow-unauthenticated `
>>     --set-env-vars GOOGLE_API_KEY="AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI" `
>>     --port=8787


 host =https://dtapi3-1021317796643.europe-west1.run.app


 docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt3-streamlit:latest -f Dockerfile .

  gcloud run deploy dt3-streamlit `   
>>     --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt3-streamlit:latest `   
>>     --platform=managed `
>>     --region=europe-west1 `
>>     --allow-unauthenticated `
>>     --port 8787