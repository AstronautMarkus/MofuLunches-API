from bson import ObjectId
from . import alimentos_bp
from utils.db_utils import get_db
from flask import request, jsonify


db = get_db()
alimentos_collection = db['alimentos']

# Get all alimentos
@alimentos_bp.route('/alimentos', methods=['GET'])
def get_alimentos():
    alimentos = list(alimentos_collection.find({}, {"_id": 0}))  # exclude _id field
    return jsonify(alimentos), 200

# Create a new alimento
@alimentos_bp.route('/alimentos', methods=['POST'])
def create_alimento():
    data = request.json
    if not data:
        return jsonify({"message": "Datos no proporcionados"}), 400
    
    missing_fields = [field for field in ["id", "nombre", "tipo"] if field not in data]
    if missing_fields:
        return jsonify({"message": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    if alimentos_collection.find_one({"id": data["id"]}):
        return jsonify({"message": "El ID ya existe"}), 400

    alimento = {
        "id": data.get("id", ""),
        "nombre": data.get("nombre", ""),
        "tipo": data.get("tipo", "")
    }

    if "nombre" in data:
        alimento["nombre"] = alimento["nombre"].capitalize()
    if "tipo" in data:
        alimento["tipo"] = alimento["tipo"].lower()  

    result = alimentos_collection.insert_one(alimento)

    # Convert ObjectId to string
    alimento["_id"] = str(result.inserted_id)
    
    return jsonify({"message": "Alimento creado exitosamente."}), 201

# Update alimento PUT 
@alimentos_bp.route('/alimentos/<string:id>', methods=['PUT'])
def update_alimento(id):
    data = request.json
    if not data:
        return jsonify({"message": "Datos no proporcionados."}), 400

    alimento = alimentos_collection.find_one({"id": id})
    if not alimento:
        return jsonify({"message": "Alimento no encontrado."}), 404

    updated_data = {}
    if "nombre" in data:
        updated_data["nombre"] = data["nombre"].capitalize()
    if "tipo" in data:
        updated_data["tipo"] = data["tipo"].lower()

    alimentos_collection.update_one({"id": id}, {"$set": updated_data})
    return jsonify({"message": "Alimento actualizado exitosamente."}), 200