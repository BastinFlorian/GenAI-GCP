FROM python:3.11

WORKDIR /app
ENV PYTHONUNBUFFERED=True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Define the port as an environment variable
ENV PORT=8501

# Expose the defined port
EXPOSE ${PORT}

COPY . ./app

# Use shell form for ENTRYPOINT to allow variable substitution
ENTRYPOINT ["sh", "-c", "streamlit run --server.port=${PORT} app/app.py --server.address=0.0.0.0"]

#ENTRYPOINT streamlit run --server.port ${PORT} app/app.py –-server.address=0.0.0.0


#errors :  - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 5)
# - JSONArgsRecommended: JSON arguments recommended for ENTRYPOINT to prevent unintended behavior related to OS signals (line 17)


#Commands : 
#Set-ExecutionPolicy Bypass -Scope Process
#docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/mm-streamlit:latest -f Dockerfile .
#gcloud run deploy mm-streamlit --image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/mm-streamlit:latest --platform=managed --region=europe-west1 --allow-unauthenticated

