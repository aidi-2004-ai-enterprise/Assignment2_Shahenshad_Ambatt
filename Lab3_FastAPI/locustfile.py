from locust import HttpUser, task, between

class PenguinUser(HttpUser):
    wait_time = between(1, 3)  # seconds between requests

    @task
    def predict_penguin(self):
        payload = {
            "island": "Biscoe",
            "bill_length_mm": 39.1,
            "bill_depth_mm": 18.7,
            "flipper_length_mm": 181,
            "body_mass_g": 3750,
            "year": 2007,
            "sex": "male"
        }
        self.client.post("/predict", json=payload)
