from flask import Blueprint, jsonify, current_app
import requests

pedidos_bp = Blueprint('pedidos', __name__)

# Get all pedidos
@pedidos_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502

# Get daily pedidos
@pedidos_bp.route('/pedidos/diarios', methods=['GET'])
def get_pedidos_diarios():
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos/diarios"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502
    
# Get daily pedidos
@pedidos_bp.route('/pedidos/diarios', methods=['GET'])
def get_pedidos_semanales():
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos/diarios"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502

# Get pedidos by RUT
@pedidos_bp.route('/pedidos/<rut>', methods=['GET'])
def get_pedidos_by_rut(rut):
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos/{rut}"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502

# Get daily pedido by RUT
@pedidos_bp.route('/pedidos/diarios/<rut>', methods=['GET'])
def get_pedidos_diarios_by_rut(rut):
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos/diarios/{rut}"
    try:
        
        response = requests.get(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502

# Create pedido
@pedidos_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos"
    try:
        
        response = requests.post(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502


# Update pedido status using cod_unico

@pedidos_bp.route('/pedidos/<cod_unico>', methods=['PUT'])
def update_pedido_status(cod_unico):
    service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/pedidos/{cod_unico}"
    try:
        
        response = requests.put(service_url)

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:

        print(f"Error al conectar con el servicio de pedidos: {e}")

        return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502
    

