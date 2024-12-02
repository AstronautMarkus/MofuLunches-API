import requests
from bson import ObjectId
from datetime import datetime
from . import pedidos_bp
from utils.db_utils import get_db
from flask import request, jsonify


class PedidosCollection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PedidosCollection, cls).__new__(cls)
            db = get_db()
            cls._instance.collection = db['pedidos']
        return cls._instance


pedidos_collection = PedidosCollection().collection

# Get pedidos full list
@pedidos_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = list(pedidos_collection.find({}))
    
    # Convert ObjectId to string
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])

    return jsonify(pedidos), 200


# Get daily pedidos
@pedidos_bp.route('/pedidos/diarios', methods=['GET'])
def get_pedidos_diarios():
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    pedidos = list(pedidos_collection.find(
        {"fecha_pedido": fecha_hoy},
        sort=[("cod_diario", 1)]
    ))
    
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])

    return jsonify(pedidos), 200

# Get all pedidos by rut
@pedidos_bp.route('/pedidos/<rut>', methods=['GET'])
def get_pedidos_by_rut(rut):
    pedidos = list(pedidos_collection.find({"rut": rut}))
    
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])

    return jsonify(pedidos), 200


# Get pedido diario by rut
@pedidos_bp.route('/pedidos/diarios/<rut>', methods=['GET'])
def get_pedidos_diarios_by_rut(rut):
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    pedidos = list(pedidos_collection.find(
        {"rut": rut, "fecha_pedido": fecha_hoy},
        sort=[("cod_diario", 1)]
    ))
    
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])

    return jsonify(pedidos), 200


# Create pedido
@pedidos_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()

    # Check fields are present
    required_fields = ['rut', 'alimentos', 'hora_retiro']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Faltan campos obligatorios en el pedido: rut, alimentos, hora_retiro."}), 400

    if not isinstance(data['alimentos'], list):
        return jsonify({"message": "El campo 'alimentos' debe ser una lista de objetos."}), 400

    for alimento in data['alimentos']:
        if not isinstance(alimento, dict) or not all(key in alimento for key in ['id', 'nombre', 'tipo']):
            return jsonify({"message": "Cada alimento debe ser un objeto con los campos 'id', 'nombre' y 'tipo'."}), 400

    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/America/Santiago")
        response.raise_for_status()
        external_time_data = response.json()
        external_datetime = datetime.fromisoformat(external_time_data['datetime'][:-1])
        external_time = external_datetime.strftime('%H:%M')
        fecha_hoy = external_datetime.strftime('%Y-%m-%d')
    except (requests.RequestException, KeyError, ValueError):
        now = datetime.now()
        external_time = now.strftime('%H:%M')
        fecha_hoy = now.strftime('%Y-%m-%d')

    pedido_existente = pedidos_collection.find_one({"rut": data['rut'], "fecha_pedido": fecha_hoy})
    if pedido_existente:
        return jsonify({"message": "El RUT ya tiene un pedido registrado para hoy."}), 400

    ultimo_pedido_hoy = pedidos_collection.find_one(
        {"fecha_pedido": fecha_hoy},
        sort=[("cod_diario", -1)]
    )
    cod_diario = int(ultimo_pedido_hoy['cod_diario']) + 1 if ultimo_pedido_hoy else 1

    ultimo_pedido_global = pedidos_collection.find_one(
        {},
        sort=[("cod_unico", -1)]
    )
    cod_unico = int(ultimo_pedido_global['cod_unico']) + 1 if ultimo_pedido_global else 1

    nuevo_pedido = {
        "rut": data['rut'],
        "fecha_pedido": fecha_hoy,
        "hora_creacion": external_time,
        "hora_retiro": data['hora_retiro'],
        "cod_diario": f"{cod_diario:03d}",
        "cod_unico": f"{cod_unico:05d}",
        "alimentos": data['alimentos'],
        "estado": "preparando",
    }

    pedido_id = pedidos_collection.insert_one(nuevo_pedido).inserted_id
    nuevo_pedido['_id'] = str(pedido_id)

    return jsonify({"message": "Pedido creado exitosamente"}), 201


# Update pedido status using cod_unico
@pedidos_bp.route('/pedidos/<cod_unico>', methods=['PUT'])
def update_pedido_status(cod_unico):
    pedido = pedidos_collection.find_one({"cod_unico": cod_unico})
    if not pedido:
        return jsonify({"message": "Pedido no encontrado"}), 404

    data = request.json

    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/America/Santiago")
        response.raise_for_status()
        external_time_data = response.json()
        external_datetime = datetime.fromisoformat(external_time_data['datetime'][:-1])
        external_time = external_datetime.strftime('%H:%M')
    except (requests.RequestException, KeyError, ValueError):
        external_time = datetime.now().strftime('%H:%M')

    if "hora_retiro" in data:
        try:
            datetime.strptime(data['hora_retiro'], '%H:%M')
            pedido['hora_retiro'] = data['hora_retiro']
        except ValueError:
            return jsonify({"message": "El formato de hora_retiro es inválido. Debe ser '%H:%M'."}), 400

    if "estado" in data:
        estado = data['estado'].strip().lower()
        estados_validos = ["preparando", "listo_para_retiro", "retirado"]
        if estado not in estados_validos:
            return jsonify({"message": f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}."}), 400
        pedido['estado'] = estado

    pedido['hora_modificacion'] = external_time
    pedido.pop('_id', None)

    pedidos_collection.update_one({"cod_unico": cod_unico}, {"$set": pedido})

    return jsonify({"message": "Pedido actualizado exitosamente", "pedido": pedido}), 200
