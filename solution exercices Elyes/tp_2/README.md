
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

### suprimer une image 
docker rmi api:latest
# il faut supprimer tout conteneur qui utilse cette image si nn ellle se supprime pas 
docker ps -a
docker stop <conteneur>
docker rm <container_name_or_id>




Build and run the FastAPI container:
```bash
docker build -t api:latest -f Dockerfile_api . # Cette commande construit une image Docker à partir du Dockerfile nommé Dockerfile_api
docker run --name fastapi-container -p 8181:8181 api:latest 
# Cette commande crée et démarre un nouveau conteneur nommé fastapi-container à partir de l'image api:latest, en mappant le port 8181 du conteneur au port 8181 de l'hôte

Pourquoi app est une Instance de FastAPI
Dans le contexte de FastAPI, le terme "instance" fait référence à un objet créé à partir d'une classe.

FastAPI() est une classe fournie par la bibliothèque FastAPI, et lorsque vous faites app = FastAPI(), vous créez une instance de cette classe.
Cette instance app est ce qui permet de définir les routes, les gestionnaires d'événements, et d'autres comportements de votre application web.
Comment cela fonctionne dans le Dockerfile
Lorsque vous configurez votre Dockerfile, vous devez spécifier quel module et quelle instance utiliser pour lancer l'application. Dans votre cas :

api:app indique que vous utilisez le module api (qui est votre fichier api.py sans l'extension .py) et que vous accédez à l'instance app à l'intérieur de ce module.

Conclusion
api.py est l'endroit où vous définissez l'instance de FastAPI, nommée app.
app.py est l'application Streamlit qui utilise cette API.

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
        --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
        --platform=managed \
        --region=<my-region> \
        --allow-unauthenticated \
        --port=8181
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
        --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-image-name>:latest \
        --platform=managed \
        --region=<my-region> \
        --allow-unauthenticated
```


DEPLOIMENT : 
 1. Préparer le déploiement FastAPI

# Construisez et poussez l'image Docker sur Google Artifact Registry :

docker buildx build --platform linux/amd64 --push `
    -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/elyes_tpd_api:latest `
    -f Dockerfile_api .

# Déployez votre image sur Google Cloud Run :

gcloud run deploy elyesapi \
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/elyes_tpd_api:latest \
    --platform=managed \
    --region=europe-west1 \
    --allow-unauthenticated \
    --port=8282

3. recuperer url
gcloud run services describe elyesapi --platform=managed --region=europe-west1 --format="value(status.url)"

changer le host dans app.py : HOST= "https://elyesapi-63idnujfwq-ew.a.run.app/answer"

2. Préparer le déploiement Streamlit
# Construisez et poussez l'image Docker sur Google Artifact Registry :

docker buildx build --platform linux/amd64 --push `
    -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/elyes_tp2_streamlit:latest `
    -f Dockerfile .

# Déployez votre image sur Google Cloud Run :

gcloud run deploy elyesstreamlit `
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/elyes_tp2_streamlit:latest `
    --platform=managed `
    --region=europe-west1 `
    --allow-unauthenticated `
    --port=8602


no ma3lich yaatini saha !    
https://elyesstreamlit-1021317796643.europe-west1.run.app/
    



