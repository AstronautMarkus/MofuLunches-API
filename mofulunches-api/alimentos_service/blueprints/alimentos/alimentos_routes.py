from bson import ObjectId
from . import alimentos_bp
from utils.db_utils import get_db
from flask import request, jsonify


class AlimentosCollection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlimentosCollection, cls).__new__(cls)
            db = get_db()
            cls._instance.collection = db['alimentos']
        return cls._instance

alimentos_collection = AlimentosCollection().collection

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
    
    # Check missing fields
    missing_fields = [field for field in ["nombre", "tipo"] if field not in data]
    if missing_fields:
        return jsonify({"message": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Get the last alimento to increment the ID
    last_alimento = alimentos_collection.find_one(
        {}, 
        sort=[("id", -1)]  # Sort by ID descending
    )
    new_id = last_alimento["id"] + 1 if last_alimento else 1  # Incrase or initialize ID

    # Create alimento object
    alimento = {
        "id": new_id,  # Autoincremental ID
        "nombre": data.get("nombre", "").capitalize(),
        "tipo": data.get("tipo", "").lower()
    }

    result = alimentos_collection.insert_one(alimento)

    # Convert to ObjectId to be able to serialize it
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