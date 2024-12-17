
## 2. Separate the Backend from the Frontend

The goal of this session is to separate the backend from the frontend. The backend will be a FastAPI that will be deployed on GCP. The frontend will be a Streamlit app that will also be deployed on GCP.

### 2.1 Create the FastAPI

- Open the `exercices/tp_2/api.py` file and edit it to create a FastAPI that will return the response to a given question from part 1.
- Modify the `exercices/tp_2/app.py` file to call the FastAPI instead of the Streamlit app.

### 2.2 Test Locally

#### A. Test the API Locally

Create a custom Docker network that both containers will use to communicate with each other.
```bash
docker network create my_network
```

Build and run the FastAPI container:
```bash
docker build -t api:latest -f Dockerfile_api .
 # Open the localhost URL given
```

Test with a curl command. Edit the localhost with the chosen PORT:
```bash
curl -X 'POST' \
    'http://localhost:8181/answer' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "What is your name?"
}'
```

You should see an error message:
```json
{"detail":[{"type":"missing","loc":["body","genre"],"msg":"Field required","input":{"name":"What is your name?"}},{"type":"missing","loc":["body","language"],"msg":"Field required","input":{"name":"What is your name?"}}]}
```

- Edit the curl command to fix the error.

You should get an answer depending on the scenario, like:
```
{"message":"Bonjour madame [name]"}
```

#### B. Test the Streamlit App Locally

Check if the Streamlit app is still working (you should configure the HOST with the API container name and its host):
```bash
# Test the Streamlit app
streamlit run app.py
# Open the localhost URL given
```

Build the Docker image and run it:
```bash
docker build -t streamlit:latest -f Dockerfile .
docker run --name streamlit-container --network my_network -p 8080:8080 streamlit:latest
# --network my_network is used to connect the container to the network created
# Open the localhost URL given
```

If you encounter an error like this:
```
ConnectionError: HTTPConnectionPool(host='fastapi-container', port=8181): Max retries exceeded with URL: /answer (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0xffff86bb9a50>: Failed to resolve 'fastapi-container' ([Errno -2] Name or service not known)"))
```

You need to add the API container to the network `my_network` to enable communication with the Streamlit app:
- Remove the API container.
- Rerun the API container specifying the network.
- Retry the app.

### 2.2.3 Test Both Apps Locally with Docker Compose

Docker Compose allows you to define and run multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

- Open the Docker Compose file and check that the ports are correctly set from the ones you used in your Docker setup.

```bash
docker-compose up --build
# Open the Streamlit localhost URL given and retest your app
```

### 2.3 Deploy Both Apps in Cloud Run

#### Deploy the FastAPI App

```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _api
# Example: Florian Bastin -> <my-docker-image-name>fb_api
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile_api .

# Be careful, the default port is 8080 for Cloud Run.
# If you encounter an error message, edit the default Cloud Run port on the interface or in the command line
gcloud run deploy <my-app-name> \
        --image=<my-region>-docker.pkg.dev/dauphine-437611/<my-registry-name>/<my-docker-image-name>:latest \
        --platform=managed \
        --region=<my-region> \
        --allow-unauthenticated \
        --port=8181

gcloud run deploy meriam-api-streamlit --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/meriam-api:latest --platform=managed --region=europe-west1--allow-unauthenticated --port=8181

```

- Change the HOST in your `app.py` to the URL of the FastAPI.
Example: `HOST = "https://fb-1021317796643.europe-west1.run.app/answer"`

#### Deploy the Streamlit App

```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _streamlit
# Example: Florian Bastin -> <my-docker-image-name>fb_streamlit
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile .

gcloud run deploy <my-app-name> \
        --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/meriam_app_streamlit:latest \
        --platform=managed \
        --region=europe-west1-docker\
        --allow-unauthenticated
```
