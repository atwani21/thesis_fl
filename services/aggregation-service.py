from flask import Flask, request, jsonify
import numpy as np
import requests

app = Flask(__name__)

MODEL_SERVICE_URL = 'http://localhost:5004'
clients = {}
global_models = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    client_id = data['client_id']
    disagreed_clients = data['disagreed_clients']
    group_id = data['group_id']
    
    if group_id not in global_models:
        global_models[group_id] = {
            'coef': np.zeros(1).tolist(),
            'intercept': [0.0]
        }

    if client_id not in clients:
        clients[client_id] = {'status': 'active', 'disagreed_clients': disagreed_clients, 'group_id': group_id}
        return jsonify({"message": f"Client {client_id} registered successfully in group {group_id}."}), 200
    else:
        return jsonify({"message": f"Client {client_id} already registered."}), 200

@app.route('/aggregate', methods=['POST'])
def aggregate():
    data = request.get_json()
    client_params = data['client_params']
    client_id = data['client_id']
    group_id = clients[client_id]['group_id']

    for client in clients:
        if client_id in clients[client]['disagreed_clients']:
            return jsonify({"message": f"Client {client_id} has disagreement with {client}. Skipping aggregation."}), 200
        if client in clients[client_id]['disagreed_clients']:
            return jsonify({"message": f"Client {client_id} has disagreement with {client}. Skipping aggregation."}), 200

    global_model = global_models[group_id]
    
    client_coef = np.array(client_params['coef'])
    client_intercept = client_params['intercept'][0]

    global_model['coef'] = ((np.array(global_model['coef']) + client_coef) / 2).tolist()
    global_model['intercept'] = [(np.array(global_model['intercept'])[0] + client_intercept) / 2]

    update_global_model(global_model['coef'], global_model['intercept'])
    return jsonify({"message": f"Model aggregated successfully for group {group_id}", "global_model": global_model})

def fetch_global_model():
    global_model_response = requests.get(f"{MODEL_SERVICE_URL}/get_global_model")
    if global_model_response.status_code == 200:
        global_model = global_model_response.json()
        coef = np.array(global_model['coef'])
        intercept = global_model['intercept'][0]
        return coef, intercept
    else:
        raise RuntimeError("Failed to fetch global model.")

def update_global_model(coef, intercept):
    data = {
        'coef': coef,
        'intercept': [intercept]
    }
    response = requests.post(f"{MODEL_SERVICE_URL}/set_global_model", json=data)
    if response.status_code == 200:
        print("Global model updated successfully.")
    else:
        print(f"Failed to update global model: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
