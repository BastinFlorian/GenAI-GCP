# How to use this repository

## Expectations from Dauphine AI students

### Evaluation criteria
- The quality of the code (add Flake8 and Pytlint linters to your settings.json and use the warning to improve your code)
- The clean code principles:
  - use the PEP8 standard
  - use the following pratices:
    - use of type hints
    - use of docstrings only if needed
    - use of classes and functions
    - one function should do one thing
- The GCP deployed applications:
  - The application should be deployed in GCP
  - The interface should be working as expected
  - You should not have mutliples applications deployed at the same time


### How to submit your work
- TODO

### Mandatory steps
- Anything you deploy, create in GCP should have your initials at the beggining
## Pre-requisites

- Python 3.11 or higher [here](https://www.python.org/downloads/)
- Conda or Miniconda [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Docker [here](https://docs.docker.com/get-docker/)
- VS Code [here](https://code.visualstudio.com/download)
- GCloud SDK [here](https://cloud.google.com/sdk/docs/install)

## Create your virtual environment

```bash
conda create --name genai_gcp python=3.11
conda activate genai_gcp
pip install -r requirements.txt
```

## Authenticate on GCP

```bash
gcloud init # Use your email and project settings
gcloud auth login
gcloud auth application-default login # Authenticate on GCP with admin account
```

## Command used ONLY by the teacher to create the required objects in GCP

- Configure API, IAM and Service Account
```bash
gcloud init # Use your email and project settings
gcloud auth application-default login # Authenticate on GCP with admin account
gcloud storage buckets create gs://<my-tfstate-bucket> --project=<my-project-id> --location=<my-region> # You need storage.buckets.create permission (ex: roles/editor)
cd terraform/bootstrap
vim backend.tf
# Edit <my-tfstate-bucket> with the name of the bucket created above
vim terraform.tfvars
# Edit the values of project_id, location, artifactregistry_name and service_account_name
terraform init # You need storage.buckets.list permission (ex: roles/storage.objectUser)
terraform apply -var gcp_account_email="<my-user-email>"
# return the service account to be copu next line
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=<my-service-account>@<my-project-id>.iam.gserviceaccount.com
```

# About the exercices

This repository contains the exercises to help you deploy a RAG application in GCP.
You will have to complete the exercises in the following order:
- `tp_1` explains how to create a basic streamlit app in CloudRun
- `tp_2` explains how to split the backend and frontend of your app and deploy in Cloud Run
- `tp_3` explains how to use Gemini LLM to create a basic question answering app without external knowledge
- `tp_4` explains how to create and fill a Cloud SQL instance with the data needed for the RAG model:
  - Loading the data in Google Cloud Storage
  - Chunking the data with Google Cloud Functions and adding it to the Cloud SQL instance
  - Updating the data with Google Cloud Functions when new data is added to the bucket
- `tp_5` explains how to use this data hosted in Cloud SQL to improve your question answering app
- `tp_6` explains how to use the RAG model to improve your question answering app
- `tp_7` explains how collect user feedback from you app and store them in BigQuery
- `tp_8` show the alternatives of architeecture that can be used to deploy the RAG model in production
  - Using Dialogflow

## Roadmap:
- Terraform Cloud SQL instance and db ingestion
- Terraform User

### Troubleshooting

You will encouters a lot of errors when developing. Don't worry it's part of the learning process.
A few hints on how to solve them:
```bash
- ERROR: Cannot connect to the Docker daemon # Docker app is not opened
- A env variable is not recongized # Check the .env file, run source .env in the terminal, load_dotenv() in the python file

```