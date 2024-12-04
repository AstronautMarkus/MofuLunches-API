from flask import Blueprint, jsonify, current_app, request
import requests

# Factory function to create the usuarios blueprint
def create_usuarios_blueprint():
    usuarios_bp = Blueprint('usuarios', __name__)

    def handle_request(endpoint, method, **kwargs):
        """
        Centralized logic to handle requests to the usuarios service.
        """
        service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(service_url, params=kwargs.get("params", {}))
            elif method == "POST":
                response = requests.post(service_url, json=kwargs.get("json", {}))
            elif method == "PUT":
                response = requests.put(service_url, json=kwargs.get("json", {}))
            elif method == "PATCH":
                response = requests.patch(service_url, json=kwargs.get("json", {}))
            elif method == "DELETE":
                response = requests.delete(service_url)
            else:
                return jsonify({"error": "Método HTTP no soportado."}), 405

            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servicio de usuarios: {e}")
            return jsonify({"error": "No se pudo conectar con el servicio de usuarios."}), 502

    # usuarios service routes
    @usuarios_bp.route('/usuarios', methods=['GET'])
    def get_users():
        return handle_request("usuarios", "GET")

    @usuarios_bp.route('/usuarios/<rut>', methods=['GET'])
    def get_user_by_rut(rut):
        return handle_request(f"usuarios/{rut}", "GET")

    @usuarios_bp.route('/usuarios', methods=['POST'])
    def create_user():
        return handle_request("usuarios", "POST", json=request.json)

    @usuarios_bp.route('/usuarios/<rut>', methods=['PUT'])
    def update_user(rut):
        return handle_request(f"usuarios/{rut}", "PUT", json=request.json)

    @usuarios_bp.route('/usuarios/<rut>', methods=['PATCH'])
    def update_user_partially(rut):
        return handle_request(f"usuarios/{rut}", "PATCH", json=request.json)


    @usuarios_bp.route('/usuarios/login', methods=['POST'])
    def login_user():
        """
        User login and special handling to include tokens in the response headers.
        """
        service_url = f"{current_app.config['USUARIOS_SERVICE_URL']}/login"
        try:
            response = requests.post(service_url, json=request.json)
            if response.status_code == 200:
                # Header tokens extraction
                access_token = response.headers.get("Authorization")
                refresh_token = response.headers.get("Refresh-Token")

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
                return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servicio de usuarios: {e}")
            return jsonify({"error": "No se pudo conectar con el servicio de usuarios."}), 502

    return usuarios_bp
