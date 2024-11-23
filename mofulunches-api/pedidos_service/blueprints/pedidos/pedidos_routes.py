import requests
from bson import ObjectId
from datetime import datetime
from . import pedidos_bp
from utils.db_utils import get_db
from flask import request, jsonify


db = get_db()
pedidos_collection = db['pedidos']

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


# Create a new pedido

db = get_db()
pedidos_collection = db['pedidos']

# ObjectID serializer
def serialize_objectid(data):
    if isinstance(data, list):  # Document list
        return [{**item, '_id': str(item['_id'])} if '_id' in item else item for item in data]
    elif isinstance(data, dict):  # Only one document
        return {**data, '_id': str(data['_id'])} if '_id' in data else data
    return data  # Any other data type


# Update pedido status using cod_unico

@pedidos_bp.route('/pedidos/<cod_unico>', methods=['PUT'])
def update_pedido_status(cod_unico):
    # Search pedido by cod_unico
    pedido = pedidos_collection.find_one({"cod_unico": cod_unico})
    if not pedido:
        return jsonify({"message": "Pedido no encontrado"}), 404

    data = request.json

    # Use API to get current time
    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/America/Santiago")
        response.raise_for_status()
        external_time_data = response.json()
        external_datetime = datetime.fromisoformat(external_time_data['datetime'][:-1])
        external_time = external_datetime.strftime('%H:%M')  
    except (requests.RequestException, KeyError, ValueError):
        external_time = datetime.now().strftime('%H:%M')  

    # Validate and update hora_retiro
    if "hora_retiro" in data:
        try:
            # Validate hora_retiro
            datetime.strptime(data['hora_retiro'], '%H:%M') 
            pedido['hora_retiro'] = data['hora_retiro']
        except ValueError:
            return jsonify({"message": "El formato de hora_retiro es inválido. Debe ser '%H:%M'."}), 400

    # Validate and update estado
    if "estado" in data:
        
        estado = data['estado'].strip().lower()

        # Check if the state is valid
        estados_validos = ["preparando", "listo_para_retiro", "retirado"]
        if estado not in estados_validos:
            return jsonify({"message": f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}."}), 400

        # Update estado
        pedido['estado'] = estado

    # Update hora_modificacion
    pedido['hora_modificacion'] = external_time

    # No _id
    pedido.pop('_id', None)

    # Update pedido
    pedidos_collection.update_one({"cod_unico": cod_unico}, {"$set": pedido})

    return jsonify({
        "message": "Pedido actualizado exitosamente",
        "pedido": pedido
    }), 200