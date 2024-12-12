from flask import Blueprint, jsonify, current_app, request
import requests

# Factory function to create the pedidos blueprint
def create_pedidos_blueprint():
    pedidos_bp = Blueprint('pedidos', __name__)

    def handle_request(endpoint, method, **kwargs):
        """
        Centralized logic to handle requests to the pedidos service.
        """
        service_url = f"{current_app.config['PEDIDOS_SERVICE_URL']}/{endpoint}"
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
            print(f"Error al conectar con el servicio de pedidos: {e}")
            return jsonify({"error": "No se pudo conectar con el servicio de pedidos."}), 502

    # Pedidos service routes
    @pedidos_bp.route('/pedidos', methods=['GET'])
    def get_pedidos():
        params = {
            "desde": request.args.get("desde"),
            "hasta": request.args.get("hasta")
        }
        return handle_request("pedidos", "GET", params=params)

    @pedidos_bp.route('/pedidos/diarios', methods=['GET'])
    def get_pedidos_diarios():
        return handle_request("pedidos/diarios", "GET")

    @pedidos_bp.route('/pedidos/<rut>', methods=['GET'])
    def get_pedidos_by_rut(rut):
        params = {
            "desde": request.args.get("desde"),
            "hasta": request.args.get("hasta")
        }
        return handle_request(f"pedidos/{rut}", "GET", params=params)

    @pedidos_bp.route('/pedidos/diarios/<rut>', methods=['GET'])
    def get_pedidos_diarios_by_rut(rut):
        return handle_request(f"pedidos/diarios/{rut}", "GET")

    @pedidos_bp.route('/pedidos', methods=['POST'])
    def create_pedido():
        return handle_request("pedidos", "POST", json=request.json)

    @pedidos_bp.route('/pedidos/<cod_unico>', methods=['PUT'])
    def update_pedido_status(cod_unico):
        return handle_request(f"pedidos/{cod_unico}", "PUT", json=request.json)

    return pedidos_bp
