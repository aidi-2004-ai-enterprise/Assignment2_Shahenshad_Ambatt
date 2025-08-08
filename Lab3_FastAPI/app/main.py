"""
FastAPI application for classifying penguin species using a trained XGBoost model.
"""
import os
from dotenv import load_dotenv
from google.cloud import storage

import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Download model from Google Cloud Storage
def download_model_from_gcs():
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    blob_name = os.getenv("GCS_BLOB_NAME")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not all([bucket_name, blob_name, credentials_path]):
        logger.error("❌ Missing environment variables for GCS access.")
        raise ValueError("GCS environment variables not set.")

    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    local_model_path = os.path.join(os.path.dirname(__file__), "data", "model.json")
    os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
    blob.download_to_filename(local_model_path)

    logger.info("✅ Model downloaded from GCS to %s", local_model_path)
    return local_model_path

# Load model
model_path = download_model_from_gcs()
model = xgb.XGBClassifier()
model.load_model(model_path)
logger.info("✅ Model loaded from %s", model_path)

# Species label mapping
species_labels = ["Adelie", "Chinstrap", "Gentoo"]

# FastAPI app
app = FastAPI(title="Penguin Classifier API")

class Island(str, Enum):
    Torgersen = "Torgersen"
    Biscoe = "Biscoe"
    Dream = "Dream"

class Sex(str, Enum):
    male = "male"
    female = "female"

class PenguinFeatures(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    year: int
    sex: Sex
    island: Island

def preprocess_features(features: PenguinFeatures) -> pd.DataFrame:
    input_dict = features.model_dump()
    df = pd.DataFrame([input_dict])

    for col, values in {
        "sex": ["male", "female"],
        "island": ["Biscoe", "Dream", "Torgersen"]
    }.items():
        for val in values:
            df[f"{col}_{val}"] = (df[col] == val).astype(int)

    df.drop(columns=["sex", "island"], inplace=True)

    expected_cols = [
        "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year",
        "sex_female", "sex_male",
        "island_Biscoe", "island_Dream", "island_Torgersen"
    ]
    return df.reindex(columns=expected_cols, fill_value=0)

@app.get("/")
def root() -> dict:
    return {"message": "Penguin Classification API running."}

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/predict")
def predict(features: PenguinFeatures) -> dict:
    try:
        X_input = preprocess_features(features)
        prediction = model.predict(X_input)[0]
        logger.info("Prediction successful: %s", prediction)
        return {
            "prediction": int(prediction),
            "species": species_labels[int(prediction)]
        }
    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        return {"error": str(e)}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
