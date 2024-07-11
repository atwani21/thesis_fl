# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Flask services
EXPOSE 5000 5002 5003 5004

# Define environment variables for each service
ENV FLASK_APP_1=model_service.py
ENV FLASK_APP_2=aggregation_service.py
ENV FLASK_APP_3=evaluate_service.py
ENV FLASK_APP_4=training_service.py

# Set up commands to run the Flask services using Supervisor
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
