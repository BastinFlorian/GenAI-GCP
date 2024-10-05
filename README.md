*# How to use this repository

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
