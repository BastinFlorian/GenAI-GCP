
## 1. Build and deploy a docker image that is a Streamlit app

The goal of this session is to create a "Hello world" streamlit interface that will be deployed on GCP. The first step is to create a docker image that will contain the streamlit application.
You need to have docker installed on your machine.

### 1.1 Local testing

A. We will first create our streamlit app and test it locally.

```bash
cd exercices/tp_1/
streamlit run app.py
# Open the url given in localhost
```

B. Edit the streamlit app to:
  - Create two buttons:
    - Language: English, French
    - Genre: Man, Woman
  - Adapt the input sentence: to ask for the name of the person
  - Adapt the output sentence:
    - For a man in English: "Hello Mr. [name]"
    - For a woman in French "Bonjour madame [name]"
    - ...
    - ...

**Hint**:
- Use st.sidebar, st.selectbox, st.text_input, st.write
- Go to the Streamlit documentation

C. Test the app locally

```bash
streamlit run app.py
# Open the url given in localhost
```

D. Use the Dockerfile to build the image

Open and edit The `Dockerfile` as required, to match with the port exposed below.
We create a Docker image that will contain the streamlit app.
The Dockerfile is already created in root folder
Look at `docker build` and `docker run` documentation
We use docker because it is mandatory to deploy an app on GCP

```bash
docker build -t streamlit:latest .
docker run --name my_container -p 8080:8080 streamlit:latest
# Open the url given
```

Once it works, you can use the following commands:
```bash
docker stop <my-container>
docker rm <my-container>
# Then you can re run docker run -p 8080:8080 streamlit:latest without any problems
# If you have a "already in use" error, do the previous steps before rerunning
```

### 1.2 Deploy on GCP
```bash
gcloud init # Use your email and project settings
gcloud auth application-default login # Authenticate on GCP with admin account

# Docker authentication
gcloud auth configure-docker europe-west1-docker.pkg.dev


# Replace <my-docker-image-name> and <my-app-name> by your initials + -streamlit
# Florian Bastin -> <my-docker-image-name>=fb-streamlit
# Replace docker buildx build --platform linux/amd64 by docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest -f Dockerfile .

gcloud run deploy <my-app-name> \
    --image=europe-west1-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
    --platform=managed \
    --region=europe-west1 \
    --allow-unauthenticated

# Open the localhost url given
```

Congratulations! You have deployed your first Streamlit app on GCP!

Our goal will be to create a chatbot in GCP.
Instead of the Hello World, we will create a bot that can answer from question from a private documentation
