from flask import Blueprint, jsonify, current_app, request
import requests

alimentos_bp = Blueprint('alimentos', __name__)

# Get all alimentos
@alimentos_bp.route('/alimentos', methods=['GET'])
def get_alimentos():
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/alimentos"
    try:
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502
    
# Get alimento by id
@alimentos_bp.route('/alimentos/<int:id>', methods=['GET'])
def get_alimento(id):
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/alimentos/{id}"
    try:
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502

# Create alimento
@alimentos_bp.route('/alimentos', methods=['POST'])
def create_alimento():
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/alimentos"
    try:
        response = requests.post(service_url, json=request.json)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502

# Update alimento by id
@alimentos_bp.route('/alimentos/<int:id>', methods=['PUT'])
def update_alimento(id):
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/alimentos/{id}"
    try:
        response = requests.put(service_url, json=request.json)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502
    
# Get all cartas
@alimentos_bp.route('/cartas', methods=['GET'])
def get_cartas():
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/cartas"

    # Get query params
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    # Set params
    params = {}
    if desde:
        params["desde"] = desde  # Send as 'desde' to the service
    if hasta:
        params["hasta"] = hasta  # Send as 'hasta' to the service

    try:
        # Request to the service
        response = requests.get(service_url, params=params)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502
    
# Get carta by id 
@alimentos_bp.route('/cartas/<int:id>', methods=['GET'])
def get_carta(id):
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/cartas/{id}"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502
    
# Create carta
@alimentos_bp.route('/cartas', methods=['POST'])
def create_carta():
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/cartas"
    try:
        response = requests.post(service_url, json=request.json)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502

# Modify carta by id 
@alimentos_bp.route('/cartas/<int:id>/alimentos', methods=['PUT'])
def modify_carta(id):
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/cartas/{id}/alimentos"
    try:
        response = requests.put(service_url, json=request.json)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502

# Rate carta by id

@alimentos_bp.route('/cartas/<int:id>/calificar', methods=['POST'])
def rate_carta(id):
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/cartas/{id}/calificar"
    try:
        response = requests.post(service_url, json=request.json)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502