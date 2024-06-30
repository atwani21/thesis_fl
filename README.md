# thesis_fl
## Overview
This project demonstrates a federated learning (FL) setup using a collection of Flask-based microservices. Each microservice handles specific tasks related to model management, training, aggregation, and evaluation. This README provides instructions on setting up and interacting with each service.

## Setup
Install Dependencies: Start by installing Python dependencies using pip. Ensure you're in the project directory containing requirements.txt.

pip install -r requirements.txt
## Run Services: Each service can be started individually. Open separate terminal windows or tabs for each service.

### Model Service (Port 5004):


python model-service.py
### Training Service (Port 5000):
python training-service.py
### FL Aggregate Service (Port 5002):
python fl-aggregate.py
### Evaluate Service (Port 5003):

python evaluate-service.py

## Verify Services: Ensure all services are running without errors and are accessible locally.

### Usage
### Model Service
Endpoint: http://localhost:5004/get_global_model
Purpose: Retrieve the global model trained through federated learning.
Training Service
Endpoint: http://localhost:5000/train
Purpose: Train a model using provided training data (X_train, y_train).
Example Usage (PowerShell/Command Prompt):

$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    X_train = @(
        @(1, 2, 3),
        @(4, 5, 6)
    )
    y_train = @(1, 2)
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/train" -Method POST -Headers $headers -Body $body
$response
### FL Aggregate Service
Endpoint: http://localhost:5002/aggregate
Purpose: Aggregate client updates using specified parameters (client_params).
Example Usage (PowerShell/Command Prompt):

$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    client_params = @{
        coef = @(0.1, 0.2, 0.3)
        intercept = @(0.4)
    }
    mode = "sequential"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5002/aggregate" -Method POST -Headers $headers -Body $body
$response
### Evaluate Service
Endpoint: http://localhost:5003/evaluate
Purpose: Evaluate a trained model using provided test data (X_test, y_test).
Example Usage (PowerShell/Command Prompt):

$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    X_test = @(
        @(1, 2, 3),
        @(4, 5, 6)
    )
    y_test = @(1, 2)
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5003/evaluate" -Method POST -Headers $headers -Body $body
$response
