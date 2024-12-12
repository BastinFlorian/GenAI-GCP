
## 1. Build and Deploy a Docker Image for a Streamlit App

The goal of this session is to create a "Hello World" Streamlit interface that will be deployed on GCP.
The first step is to create a Docker image that will contain the Streamlit application. You need to have Docker installed on your machine.

### 1.1 Local Testing

**A. Create and Test the Streamlit App Locally**

```bash
cd exercices/tp_1/
streamlit run app.py
# Open the URL given in localhost
```

**B. Edit the Streamlit App**

- Create two buttons:
    - Language: English, French
    - Gender: Man, Woman
- Adapt the input sentence to ask for the name of the person.
- Adapt the output sentence:
    - For a man in English: "Hello Mr. [name]"
    - For a woman in French: "Bonjour madame [name]"
    - ...

**Hint**:
- Use `st.sidebar`, `st.selectbox`, `st.text_input`, `st.write`
- Refer to the Streamlit documentation

**C. Test the App Locally**

```bash
streamlit run app.py
# Open the URL given in localhost
```

**D. Build the Docker Image**

Open and edit the `Dockerfile` as required to match the port exposed below. We create a Docker image that will contain the Streamlit app. The Dockerfile is already created in the root folder. Refer to the `docker build` and `docker run` documentation. We use Docker because it is mandatory to deploy an app on GCP.

```bash
docker build -t streamlit:latest .
docker run --name my_container -p 8080:8080 streamlit:latest
# Open the URL given
```

Once it works, you can use the following commands:

```bash
docker stop <my_container>
docker rm <my_container>
# Then you can rerun docker run -p 8080:8080 streamlit:latest without any problems
# If you have an "already in use" error, do the previous steps before rerunning
```

### 1.2 Deploy on GCP

```bash
gcloud init # Use your email and project settings
gcloud auth application-default login # Authenticate on GCP with admin account

# Docker authentication
gcloud auth configure-docker europe-west1-docker.pkg.dev

# Replace <my-docker-image-name> and <my-app-name> with your initials + -streamlit
# Example: Florian Bastin -> <my-docker-image-name>=fb-streamlit
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest -f Dockerfile .

gcloud run deploy <my-app-name> \
        --image=europe-west1-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
        --platform=managed \
        --region=europe-west1 \
        --allow-unauthenticated

# Open the URL given
```

Congratulations! You have deployed your first Streamlit app on GCP!

Our goal now will be to create a chatbot in GCP.
Instead of the Hello World, we will create a bot that can answer questions from private documentation.
