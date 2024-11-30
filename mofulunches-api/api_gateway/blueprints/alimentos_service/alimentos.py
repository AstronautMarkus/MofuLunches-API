from flask import Blueprint, jsonify, current_app, request
import requests

# Factory function to create the alimentos blueprint
def create_alimentos_blueprint():
    alimentos_bp = Blueprint('alimentos', __name__)

    def handle_request(endpoint, method, **kwargs):
        """
        Centralized logic to handle requests to the alimentos service.
        """
        service_url = f"{current_app.config['ALIMENTOS_SERVICE_URL']}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(service_url, params=kwargs.get("params", {}))
            elif method == "POST":
                response = requests.post(service_url, json=kwargs.get("json", {}))
            elif method == "PUT":
                response = requests.put(service_url, json=kwargs.get("json", {}))
            elif method == "DELETE":
                response = requests.delete(service_url)
            else:
                return jsonify({"error": "Método HTTP no soportado."}), 405

            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servicio de alimentos: {e}")
            return jsonify({"error": "No se pudo conectar con el servicio de alimentos."}), 502

    # CRUD default routes
    @alimentos_bp.route('/alimentos', methods=['GET'])
    def get_alimentos():
        return handle_request("alimentos", "GET")

    @alimentos_bp.route('/alimentos/<int:id>', methods=['GET'])
    def get_alimento(id):
        return handle_request(f"alimentos/{id}", "GET")

    @alimentos_bp.route('/alimentos', methods=['POST'])
    def create_alimento():
        return handle_request("alimentos", "POST", json=request.json)

    @alimentos_bp.route('/alimentos/<int:id>', methods=['PUT'])
    def update_alimento(id):
        return handle_request(f"alimentos/{id}", "PUT", json=request.json)

    # Specific "cartas" routes
    @alimentos_bp.route('/cartas', methods=['GET'])
    def get_cartas():
        params = {
            "desde": request.args.get("desde"),
            "hasta": request.args.get("hasta")
        }
        return handle_request("cartas", "GET", params={k: v for k, v in params.items() if v})

    @alimentos_bp.route('/cartas/<int:id>', methods=['GET'])
    def get_carta(id):
        return handle_request(f"cartas/{id}", "GET")

    @alimentos_bp.route('/cartas', methods=['POST'])
    def create_carta():
        return handle_request("cartas", "POST", json=request.json)

    @alimentos_bp.route('/cartas/<int:id>/alimentos', methods=['PUT'])
    def modify_carta(id):
        return handle_request(f"cartas/{id}/alimentos", "PUT", json=request.json)

    @alimentos_bp.route('/cartas/<int:id>/calificar', methods=['POST'])
    def rate_carta(id):
        return handle_request(f"cartas/{id}/calificar", "POST", json=request.json)

    return alimentos_bp
