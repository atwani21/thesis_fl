#!/bin/bash

# Function to start a service
start_service() {
    service_file=$1
    port=$2

    echo "Starting service $service_file on port $port"

    # Create a virtual environment if it doesn't exist
    if [ ! -d "venv_$port" ]; then
        python3 -m venv venv_$port
    fi

    # Activate the virtual environment
    source venv_$port/bin/activate

    # Install Flask if not already installed
    pip install flask

    # Run the Flask app on the specified port
    FLASK_APP=$service_file FLASK_ENV=development flask run --port=$port &

    # Deactivate the virtual environment
    deactivate
}

# Start Training Service
start_service "training-service.py" 5000

# Start Model Service
start_service "model-service.py" 5004

# Start Evaluate Service
start_service "evaluate-service.py" 5003

# Start Aggregation Service
start_service "aggregation-service.py" 5002

# Wait for all background processes to finish
wait

echo "All services started."
