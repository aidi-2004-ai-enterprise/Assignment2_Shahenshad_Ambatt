# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# copy the GCP key into the image
COPY gcp/sa-key.json /app/gcp/sa-key.json

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
