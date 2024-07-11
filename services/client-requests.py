import requests
import json
import numpy as np
import pandas as pd
import h5py

# Function to train the client model and return the parameters
def train_client(X_train, y_train):
    X_train_list = X_train.values.tolist()
    y_train_list = y_train.values.tolist()
    
    payload = {'X_train': X_train_list, 'y_train': y_train_list}
    response = requests.post("http://localhost:5000/train", json=payload)
    if response.status_code == 200:
        print("Training completed successfully.")
        return response.json()  # Return the client parameters
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to send client parameters and aggregate them
def aggregate_models(client_params, client_id, mode='sequential'):
    payload = {'client_params': client_params, 'client_id': client_id, 'mode': mode}
    response = requests.post("http://localhost:5002/aggregate", json=payload)
    if response.status_code == 200:
        print("Aggregation done successfully.")
    else:
        print(f"Error: {response.status_code}")

# Function to evaluate the global model
def evaluate_global_model(X_test, y_test):
    global_model_response = requests.get("http://localhost:5004/get_global_model")
    if global_model_response.status_code == 200:
        global_model = global_model_response.json()
        payload = {'X_test': X_test.values.tolist(), 'y_test': y_test.values.tolist(), 'global_model': global_model}
        response = requests.post("http://localhost:5003/evaluate", json=payload)
        if response.status_code == 200:
            print("Evaluation done successfully.")
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
    else:
        print(f"Error fetching global model: {global_model_response.status_code}")

# Function to register the client with disagreed clients and define groups
def register_client(client_id, disagreed_clients, group_id):
    payload = {'client_id': client_id, 'disagreed_clients': disagreed_clients, 'group_id': group_id}
    response = requests.post("http://localhost:5002/register", json=payload)
    if response.status_code == 200:
        print(f"Client {client_id} registered successfully.")
    else:
        print(f"Error registering client {client_id}: {response.status_code}")

if __name__ == '__main__':
    # Define the number of communication rounds
    NUM_ROUNDS = 1
    
    # Define client groups based on their agreements
    client_groups = {
        'group_1': {'clients': ['client_1', 'client_2'], 'disagreements': {'client_2': ['client_3']}},
        'group_2': {'clients': ['client_1', 'client_3'], 'disagreements': {'client_3': ['client_2']}}
    }
    
    # Iterate over each group
    for group_id, group_info in client_groups.items():
        clients = group_info['clients']
        disagreements = group_info['disagreements']
        
        # Register clients and handle disagreements
        for client_id in clients:
            disagreed_clients = disagreements.get(client_id, [])
            register_client(client_id, disagreed_clients, group_id)
        
        # Load and process datasets for each client
        for client_id in clients:
            file = f'services/datasets/{client_id}.h5'  # Adjust the file path as per your dataset structure
            
            with h5py.File(file, 'r') as hdf:
                dev_data = np.array(hdf.get('dev_data'))
                column_name = [col.decode('utf-8') for col in hdf.get('column_name')]
                test_data = np.array(hdf.get('test_data'))
    
                df_train = pd.DataFrame(data=dev_data, columns=column_name)
                df_test = pd.DataFrame(data=test_data, columns=column_name)
    
                X_train = df_train.drop(columns=["RUL"])  # Features
                y_train = df_train['RUL']  # Target variable
                X_test = df_test.drop(columns=["RUL"])  # Features
                y_test = df_test['RUL']  # Target variable
    
                for round in range(NUM_ROUNDS):
                    print(f"Starting communication round {round + 1}/{NUM_ROUNDS} for client {client_id} in group {group_id}")
    
                    # Train client and get parameters
                    client_params = train_client(X_train, y_train)
                    
                    # Aggregate client parameters after each training
                    if client_params:
                        aggregate_models(client_params, client_id, mode='sequential')
                        evaluate_global_model(X_test, y_test)
