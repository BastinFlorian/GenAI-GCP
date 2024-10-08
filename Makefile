ENV ?= development
VERSION ?= latest
REGION ?= europe-west1
AR_NAME ?= dauphine-ar
API_CONTAINER_NAME ?= fb-api
PROJECT_ID ?= dauphine-437611
API_CLOUD_RUN_NAME ?= fb-api


build-docker-streamlit:
	docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb:latest -f Dockerfile_streamlit ..

deploy-cloud-run:
	gcloud run deploy fb \
		--image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb:latest \
		--platform=managed \
		--region=europe-west1 \
		--allow-unauthenticated

build-and-deply-cloudrun-api:
	# Build and push FastAPI image
	docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb-api:latest -f Dockerfile_api .

	gcloud run deploy fb-api \
		--image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb-api:latest \
		--platform=managed \
		--region=europe-west1 \
		--allow-unauthenticated \
		--set-env-vars GOOGLE_API_KEY=[GOOGLE_API_KEY],DB_PASSWORD=[DB_PASSWORD]\
		--port=8181

build-and-deply-cloudrun-streamlit:
	# Build and push Streamlit image
	docker buildx build --platform linux/amd64 --push -t europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb-streamlit:latest .

	gcloud run deploy fb-streamlit \
		--image=europe-west1-docker.pkg.dev/dauphine-437611/dauphine-ar/fb-streamlit:latest \
		--platform=managed \
		--region=europe-west1 \
		--allow-unauthenticated

update-cloud-run:
	gcloud run services update $(API_CLOUD_RUN_NAME) --image=$(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(AR_NAME)/$(API_CONTAINER_NAME):latest --region=$(REGION)