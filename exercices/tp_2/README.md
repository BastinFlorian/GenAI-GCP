
## 2. Separate the backend from the frontend

The goal of this session is to separate the backend from the frontend.
The backend will be a Fast API that will be deployed on GCP.
The frontend will be a Streamlit app that will be deployed on GCP.

### 2.1 Create the Fast API

- Open the exercices/tp_2/api.py file and edit to create a Fast API that will return the response to a given question from part 1
- Modify the exercices/tp_2/app.py file to call the Fast API instead of the Streamlit app

### 2.2 Test locally

#### 2.2.1 Test locally the api
Create a custom Docker network that both containers will use to communicate with each other.
```bash
docker network create my_network
```

Edit the docker TODO

```bash
docker build -t api:latest -f Dockerfile_api .
docker run --name fastapi-container -p 8181:8181 api:latest
# Open the localhost url given
```

Test with a curl command
Edit the localhost with the chosen PORT
```bash
curl -X 'POST' \
  'http://localhost:8181/answer' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "What is your name?"
}'
```

You should have an error message:
```json
{"detail":[{"type":"missing","loc":["body","genre"],"msg":"Field required","input":{"name":"What is your name?"}},{"type":"missing","loc":["body","language"],"msg":"Field required","input":{"name":"What is your name?"}}]}
```

Edit the the curl command to fix the error:
```bash
# TODO
```

You should have an answer depending on the scenario like:
```
{"message":"Bonjour madame [name]"}%
```

#### 2.2.1 Test locally the streamlit app

Check if the streamlit app is still working (you should configure the HOST with the API container name and its host)
```bash
# Test the Streamlit app
streamlit run app.py
# Open the localhost url given
```

Build the docker image and run it
```bash
docker build -t streamlit:latest -f Dockerfile .
docker run --name streamlit-container --network my_network -p 8080:8080 streamlit:latest
# --network my_network is used to connect the container to the network created
# Open the localhost url given
```

```
Error:
ConnectionError: HTTPConnectionPool(host='fastapi-container', port=8181): Max retries exceeded with url: /answer (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0xffff86bb9a50>: Failed to resolve 'fastapi-container' ([Errno -2] Name or service not known)"))
```

You have to add the API container in the newtork `my_network` to be able to communicate with the streamlit app:
- Remove the API container
- Rerun the API container specifying the network
- Retry the app


### 2.2.2. Test locally both apps with docker compose

Docker Compose allows you to define and run multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

- Open the docker compose file and check that the ports are correctly set from the ones you used in your docker

```bash
docker-compose up --build
# Open the streamlit localhost url given and re test your app
```

### 2.3. Deploy both apps in CloudRun

- Deploy the Fast API app
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> by your initials + _api
# Florian Bastin -> <my-docker-image-name>fb_api
# Replace docker buildx build --platform linux/amd64 by docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile_api .

# Be careful, the default port is 8080 for Cloud Run.
# If you have an error message, edit the default Cloud RUN port on the interface or in command line
gcloud run deploy <my-app-name> \
    --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
    --platform=managed \
    --region=<my-region> \
    --allow-unauthenticated \
    --port=8181
```

- Change the HOST in you streamlit app.py to the url of the Fast API
Example: `HOST = "https://fb-1021317796643.europe-west1.run.app/answer"`

- Deploy the Streamlit app
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> by your initials + _streamlit
# Florian Bastin -> <my-docker-image-name>fb_streamlit
# Replace docker buildx build --platform linux/amd64 by docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile .

gcloud run deploy <my-app-name> \
    --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
    --platform=managed \
    --region=<my-region> \
    --allow-unauthenticated
```

