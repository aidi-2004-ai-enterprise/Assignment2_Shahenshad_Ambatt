# Deployment Guide

## 1. Overview
This document explains the complete process I followed to containerize my FastAPI + XGBoost application and deploy it to **Google Cloud Run**.  
It includes all commands I used, any issues I faced, and how I solved them. The final deployed service URL is provided at the end.

---

## 2. Containerization Process

### Step 1 – Create `Dockerfile`
I wrote a `Dockerfile` to package my app into a container image:

```dockerfile
# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
3. Preparing Google Cloud Resources
Created a Google Cloud project – My First Project.

Enabled required APIs:

Cloud Run API

Artifact Registry API

Cloud Storage API

Created a Google Cloud Storage bucket (penguin-models-ambatt) and uploaded model.json.

Created a service account penguin-api-sa and assigned the Storage Object Viewer role.

Downloaded the service account key JSON file and renamed it to sa-key.json.

Placed it inside gcp/ directory in my project.

4. Building and Pushing the Container

Step 1 – Authenticate Docker with Google Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

Step 2 – Build the Docker image
docker build -t us-central1-docker.pkg.dev/dev-spirit-468220-u4/penguin-api/penguin-app .

Step 3 – Push the image to Artifact Registry
docker push us-central1-docker.pkg.dev/dev-spirit-468220-u4/penguin-api/penguin-app

5. Deploying to Cloud Run
I used the following command to deploy the container:

gcloud run deploy penguin-service \
  --image=us-central1-docker.pkg.dev/dev-spirit-468220-u4/penguin-api/penguin-app \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCS_BUCKET_NAME=penguin-models-ambatt \
  --set-env-vars GCS_BLOB_NAME=model.json \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/gcp/sa-key.json


6. Issues Encountered & Solutions
Issue 1 – GCP permissions error when loading model

Cause: My service account did not have access to the bucket.

Solution: Assigned the Storage Object Viewer role to the service account.

Issue 2 – Missing service account credentials inside container

Cause: The sa-key.json file was not copied into the Docker image.

Solution: Created gcp/ folder, moved the key file there, and added this line in Dockerfile:
COPY gcp/sa-key.json /app/gcp/sa-key.json

Issue 3 – Deployment failed because model download happened at import time

Cause: The app tried to load the model before Cloud Run initialized.

Solution: Moved the model download logic into FastAPI's startup_event so it loads after the app starts.

7. Final Deployment
The service was successfully deployed to Cloud Run.
Final Service URL:
https://penguin-service-895961878733.us-central1.run.app