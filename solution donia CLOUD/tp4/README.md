uvicorn api:app --host 127.0.0.1 --port 8181

## 4. Ingest Your Data into a Cloud SQL Database

The goal of this session is to ingest our knowledge base into a Cloud SQL database. The data are the Gen AI Dauphine Tunis Google Slides.

We will skip the following steps:
- Creating a Cloud SQL database
- Inserting data into the Cloud SQL database
- Creating a PG vector extension in the Cloud SQL database

This [tutorial](https://python.langchain.com/docs/integrations/vectorstores/google_cloud_sql_pg/) will help you complete this exercise.

### I. Read and Download Files from Google Cloud Storage
- Open `tp_4/gcs_to_cloudsql.ipynb` and fill in the TODOs of I.

### II. Test Locally the Streamlit App and the API
- Open `tp_4/gcs_to_cloudsql.ipynb` and fill in the TODOs of II.
    - Add the merged document to a table in the Cloud SQL database

**Goal:**

![TP 4.1](../../docs/tp_4_1.png)

The created table should look like this:

![TP 4.2](../../docs/tp_4_2.png)

### III. Create a Python File to Automate the Process

Create a Python file to automate the process of ingesting the data into Cloud SQL.
1. Open the file `exercices/tp_4/ingest.py` and create the following functions:
    - List all the files in the bucket
    - Download a file locally
    - Load the content of the file with `unstructured`
    - Merge the content of the file by page
    - Create a table if the table doesn't exist
    - Get embeddings methods
    - Ingest the data into the table
    - Create a `store` instance

2. Open the file `exercices/tp_4/retrieve.py` and create the following functions:
    - Perform a similarity search

To verify the correctness of your code, you can run the following commands:
```bash
python ingest.py
python retrieve.py
```

### IV. Edit the API to Perform a Similarity Search

- Open `tp_4/api.py` and fill in the TODOs.

Hint: You can use the tests in `ingest.py` and `retrieve.py` to edit `api.py`.

You need to:
- Create a Cloud SQL connection
- Perform a similarity search from a user query
- Edit the root `get_sources` API route function to return the relevant documents

### V. Test the API

- Open `tp_4/app.py` and fill in the TODOs.

### VI. Test Locally

- Launch the API: `uvicorn api:app --host 0.0.0.0 --port 8181`
- Set the HOST in `app.py`
- Launch the app: `streamlit run app.py`

Here we just display the relevant documents from a user query. We don't ask the LLM to answer from these documents.

### VII. Deploy the API

- Deploy the FastAPI app:
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _api
# Example: Florian Bastin -> <my-docker-image-name>fb_api
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile_api .

# Be careful, the default port is 8080 for Cloud Run.
# If you encounter an error, edit the default Cloud Run port on the interface or via command line
gcloud run deploy <my-app-name> \
    --image=<my-region>-docker.pkg.dev/<my-project-id>/<my-registry-name>/<my-docker-name>:latest \
    --platform=managed \
    --region=<my-region> \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=[INSERT_GOOGLE_API_KEY],DB_PASSWORD=[INSERT_DB_PASSWORD] \
    --port 8181

# Note that a SECRET KEY like this should be provided by GOOGLE SECRET MANAGER for more safety.
# For simplicity, we will use the env variable here.
```

- Change the HOST in your Streamlit `app.py` to the URL of the FastAPI:
Example: `HOST = "https://fb-1021317796643.europe-west1.run.app/answer"`

- Deploy the Streamlit app:
```bash
# May change depending on your platform
# Replace <my-docker-image-name> and <my-app-name> with your initials + _streamlit
# Example: Florian Bastin -> <my-docker-image-name>fb_streamlit
# Replace docker buildx build --platform linux/amd64 with docker build -t if it does not work
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<my-docker-name>:latest -f Dockerfile .

gcloud run deploy <initials>-streamlit \
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/<initials>-streamlit:latest \
    --platform=managed \
    --region=europe-west1 \
    --allow-unauthenticated \
    --port 8080
```
---------------------------
---------------------------
----------------------------
docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt4api:latest -f Dockerfile_api .

2. ETAPE :

gcloud run deploy dt4api `
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt4api:latest `
    --platform=managed `
    --region=europe-west1 `
    --allow-unauthenticated `
    --set-env-vars "GOOGLE_API_KEY=AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI,DB_PASSWORD=|Q46Tr^tTqB8hSpO" `
    --port 8181


 besh ya3tik : https://elyesragapi-1021317796643.europe-west1.run.app/answer


 docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt4-treamlit:latest -f Dockerfile .   

 gcloud run deploy dt4-streamlit `
    --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/dt4-treamlit:latest `
    --platform=managed `
    --region=europe-west1 `
    --allow-unauthenticated `
    --port 8080


