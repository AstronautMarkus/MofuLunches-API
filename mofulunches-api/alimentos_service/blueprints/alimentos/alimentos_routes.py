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

# Get alimento by ID
@alimentos_bp.route('/alimentos/<int:id>', methods=['GET'])
def get_alimento(id):
    # Convertir el ID a un número entero y buscarlo en la colección
    alimento = alimentos_collection.find_one({"id": id}, {"_id": 0})
    if not alimento:
        return jsonify({"message": "Alimento no encontrado."}), 404
    return jsonify(alimento), 200



# Create a new alimento
@alimentos_bp.route('/alimentos', methods=['POST'])
def create_alimento():
    data = request.json

    if not data:
        return jsonify({"message": "Datos no proporcionados"}), 400
    
    # Missing fields
    missing_fields = [field for field in ["nombre", "tipo"] if field not in data]
    if missing_fields:
        return jsonify({"message": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Generate ID
    id_counter = db["counters"]  # Collection counters
    counter = id_counter.find_one_and_update(
        {"_id": "alimento_id"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,  # Create if not exists
        return_document=True
    )
    new_id = counter.get("sequence_value", 1)

    alimento = {
        "id": new_id,  # Autoincremental
        "nombre": data.get("nombre", "").capitalize(),
        "tipo": data.get("tipo", "").lower()
    }

    result = alimentos_collection.insert_one(alimento)

    # Convert ObjectId to string
    alimento["_id"] = str(result.inserted_id)

    return jsonify({"message": "Alimento creado exitosamente.", "alimento": alimento}), 201


# Update alimento PUT 
@alimentos_bp.route('/alimentos/<int:id>', methods=['PUT'])
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