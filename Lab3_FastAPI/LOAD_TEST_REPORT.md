# Load Test Report

## Test Overview
A load test was conducted on the deployed **Penguin Classifier API** hosted on Google Cloud Run to evaluate the performance and stability of the `/predict` endpoint under moderate request volume.

The testing was performed using Locust 2.38.0. The goal was to send repeated POST requests with a sample JSON payload to measure response times, throughput, and error rates.

---

## Test Configuration
The test simulated a single user making continuous requests to the `/predict` endpoint at a spawn rate of one user per second. The duration of the test was approximately one minute.

Sample payload used:
```json
{
  "island": "Biscoe",
  "bill_length_mm": 39.1,
  "bill_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750,
  "year": 2007,
  "sex": "male"
}
Base URL tested:
https://penguin-service-895961878733.us-central1.run.app/predict

Results Summary
A total of 31 requests were sent to the API during the test. There were no failures recorded, resulting in a 0% error rate.
The median response time was around 50 milliseconds. The 95th percentile was 66 milliseconds, and the 99th percentile was 180 milliseconds. The average response time across all requests was approximately 54.99 milliseconds.
The fastest recorded response time was 45 milliseconds, while the slowest was 177 milliseconds. The test achieved a throughput of about 0.6 requests per second, with each response averaging 35 bytes in size.

Analysis
The API demonstrated excellent stability during the test, with zero failed requests. Response times were consistently low, with most requests completing in well under 100 milliseconds. These results suggest that the current deployment can handle the tested load efficiently.
Given that this was a low-concurrency test, it is likely that the API will perform well with higher traffic, especially with Cloud Run's autoscaling capabilities.

Recommendations
Conduct tests with higher concurrency levels (e.g., 50–100 users) to evaluate performance under heavier loads.

Use varied payloads to ensure prediction accuracy across different input scenarios.

Implement GCP monitoring and alerting for real-time tracking of API health and performance.

Perform long-duration soak testing to confirm stability over extended periods.

Test Date: August 7, 2025
Tester: Shahenshad Ambatt
