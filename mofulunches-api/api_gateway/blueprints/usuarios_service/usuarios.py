from flask import Blueprint, jsonify, current_app, request
import requests

usuarios_bp = Blueprint('usuarios', __name__)

# 1. Gell all users
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_users():
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/usuarios"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de usuarios: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de usuarios."}), 502


# 2. Get users by rut
@usuarios_bp.route('/usuarios/<rut>', methods=['GET'])
def get_user_by_rut(rut):
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/usuarios/{rut}"
    try:
        response = requests.get(service_url)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Servicio de usuarios no disponible."}), 500


# 3. Create user
@usuarios_bp.route('/usuarios', methods=['POST'])
def create_user():
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/usuarios"
    try:
        # Forward the POST request to the user service
        response = requests.post(service_url, json=request.json)
        # Reuturn json response and status code
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        # Error handling
        return jsonify({"error": "Servicio de usuarios no disponible."}), 500


# 4. Update user fully
@usuarios_bp.route('/usuarios/<rut>', methods=['PUT'])
def update_user(rut):
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/usuarios/{rut}"
    try:
        response = requests.put(service_url, json=request.json)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de usuarios: {e}")
        return jsonify({"error": "Servicio de usuarios no disponible."}), 500


# 5. Update user partially
@usuarios_bp.route('/usuarios/<rut>', methods=['PATCH'])
def update_user_partially(rut):
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/usuarios/{rut}"
    try:
        response = requests.patch(service_url, json=request.json)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de usuarios: {e}")
        return jsonify({"error": "Servicio de usuarios no disponible."}), 500


# 6. Login user
@usuarios_bp.route('/usuarios/login', methods=['POST'])
def login_user():
    service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/login"
    try:
        
        response = requests.post(service_url, json=request.json)
        
        # Get tokens from the user service
        if response.status_code == 200:
            # Extract tokens from the response headers
            access_token = response.headers.get("Authorization")
            refresh_token = response.headers.get("Refresh-Token")

            # Modify the response to include the tokens
            response_data = response.json()
            return (
                jsonify(response_data),
                200,
                {
                    "Authorization": access_token,
                    "Refresh-Token": refresh_token
                }
            )
        else:
            # All errors are returned as JSON
            return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de usuarios: {e}")
        return jsonify({"error": "Servicio de usuarios no disponible."}), 500