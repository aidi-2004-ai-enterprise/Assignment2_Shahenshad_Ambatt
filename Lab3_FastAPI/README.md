# Penguin Classification API

## 1. Project Overview
This project is a **FastAPI** application that classifies penguin species based on input features using a pre-trained **XGBoost** model.  
The application is containerized with **Docker** and deployed to **Google Cloud Run**.  
The model file (`model.json`) is stored in a Google Cloud Storage (GCS) bucket and loaded at application startup.

---

## 2. Setup Instructions

### Prerequisites
- Python 3.10+
- Docker
- Google Cloud SDK (`gcloud`)
- Access to a GCS bucket containing the model file

### Local Setup
1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd <repo_name>

Install dependencies

pip install -r requirements.txt
Run locally


uvicorn app.main:app --host 0.0.0.0 --port 8080
3. Deployment Instructions (Cloud Run)
Build and Push Image

docker build -t us-central1-docker.pkg.dev/<project-id>/<repo>/<image-name> .
docker push us-central1-docker.pkg.dev/<project-id>/<repo>/<image-name>
Deploy to Cloud Run

gcloud run deploy penguin-service \
  --image=us-central1-docker.pkg.dev/<project-id>/<repo>/<image-name> \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCS_BUCKET_NAME=penguin-models-ambatt \
  --set-env-vars GCS_BLOB_NAME=model.json \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/gcp/sa-key.json

4. API Documentation
Base URL

https://penguin-service-895961878733.us-central1.run.app
Endpoints
GET /docs
Opens the Swagger UI for interactive API exploration.

POST /predict
Classifies the penguin species based on input features.

Request Body Example:


{
  "island": "Biscoe",
  "bill_length_mm": 39.1,
  "bill_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750,
  "sex": "male"
}
Response Example:

{
  "species": "Adelie"
}


5. Answers to Provided Questions
Q1: What edge cases might break your model in production that aren't in your training data?

Completely new penguin species not seen during training.

Extreme outlier measurements (e.g., unrealistic bill lengths).

Missing or malformed feature values.

Q2: What happens if your model file becomes corrupted?

The API will fail to load the model at startup and return errors for /predict.

A proper fix would be to add file integrity checks and a fallback model.

Q3: What's a realistic load for a penguin classification service?

Around 50–200 requests per second for a small Cloud Run instance, depending on memory and CPU allocation.

Q4: How would you optimize if response times are too slow?

Increase Cloud Run CPU/memory allocation.

Cache model in memory after load.

Batch process requests where possible.

Q5: What metrics matter most for ML inference APIs?

Response time (latency)

Throughput (requests per second)

Error rate

Model accuracy and prediction distribution

Q6: Why is Docker layer caching important for build speed? (Did you leverage it?)

Caching allows unchanged layers to be reused, significantly reducing build time.

Yes, by installing dependencies after copying requirements.txt, builds are faster.

Q7: What security risks exist with running containers as root?

If the container is compromised, attackers could gain host-level access.

Best practice: use a non-root user in Dockerfile.

Q8: How does cloud auto-scaling affect your load test results?

Auto-scaling can hide latency spikes because more instances are spawned.

Initial cold starts may cause temporary slowdowns.

Q9: What would happen with 10x more traffic?

More Cloud Run instances would spin up (if limits allow).

Costs would increase proportionally.

Cold starts would become more noticeable.

Q10: How would you monitor performance in production?

Use Google Cloud Monitoring & Logging to track latency, error rates, and resource usage.

Q11: How would you implement blue-green deployment?

Deploy a new revision (green) alongside the existing one (blue).

Gradually shift traffic to the new version.

Roll back if issues occur.

Q12: What would you do if deployment fails in production?

Roll back to the previous stable revision in Cloud Run.

Check logs to debug the failure before retrying.

Q13: What happens if your container uses too much memory?

Cloud Run will terminate the container with an OOM (Out Of Memory) error.

Fix by optimizing memory usage or increasing allocated memory.


6. Final Service URL

https://penguin-service-895961878733.us-central1.run.app/docs