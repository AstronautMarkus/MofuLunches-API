from flask import Blueprint, jsonify, current_app, request
import requests

alimentos_bp = Blueprint('alimentos', __name__)

# 1. Gell all users
@alimentos_bp.route('/alimentos', methods=['GET'])
def get_users():
    service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/alimentos"
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
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de alimentos: {e}")

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
