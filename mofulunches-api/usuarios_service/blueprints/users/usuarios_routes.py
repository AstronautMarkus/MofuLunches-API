from flask import request, jsonify
from . import users_bp
from utils.db_utils import get_db

db = get_db()
users_collection = db['usuarios']

# Get all users
@users_bp.route('/usuarios', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # no ID field
    return jsonify(users), 200

# Get user by RUT
@users_bp.route('/usuarios/<rut>', methods=['GET'])
def get_user_by_rut(rut):
    user = users_collection.find_one({"rut": rut}, {"_id": 0})
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Usuario no encontrado."}), 404

# Update user
@users_bp.route('/usuarios/<rut>', methods=['PUT'])
def update_user(rut):
    data = request.json
    result = users_collection.update_one({"rut": rut}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Usuario actualizado exitosamente."}), 200
    return jsonify({"error": "User not found"}), 404

# Delete user
@users_bp.route('/usuarios/<rut>', methods=['DELETE'])
def delete_user(rut):
    result = users_collection.delete_one({"rut": rut})
    if result.deleted_count:
        return jsonify({"message": "Usuario eliminado exitosamente."}), 200
    return jsonify({"error": "Usuario no encontrado."}), 404

# Create user with RUT verification
@users_bp.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    
    # Required fields
    required_fields = ["rut", "Nombres", "apellidos", "correo", "contrasena", "codigo_RFID", "tipo_usuario"]
    
    # Check missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Check if RUT already exists
    if users_collection.find_one({"rut": data["rut"]}):
        return jsonify({"error": "El RUT ya existe."}), 400

    # Insert user
    users_collection.insert_one(data)
    return jsonify({"message": "Usuario creado exitosamente."}), 201
