from . import users_bp
from utils.db_utils import get_db
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash


db = get_db()
users_collection = db['usuarios']

# Get all users
@users_bp.route('/usuarios', methods=['GET'])

def get_users():
    users = list(users_collection.find({}, {"_id": 0, "contrasena": 0}))  # exclude password field
    return jsonify(users), 200

# Get user by RUT
@users_bp.route('/usuarios/<rut>', methods=['GET'])

def get_user_by_rut(rut):
    user = users_collection.find_one({"rut": rut}, {"_id": 0, "contrasena": 0})  # exclude password field
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

# Create user with RUT verification and hashed password
@users_bp.route('/usuarios', methods=['POST'])

def create_user():
    data = request.json
    
    # Required fields
    required_fields = ["rut", "nombre", "apellido", "correo", "contrasena", "codigo_RIFD", "tipo_usuario"]
    
    # Check missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Check if RUT already exists
    if users_collection.find_one({"rut": data["rut"]}):
        return jsonify({"error": "El RUT ya existe."}), 400

    # Normalize data
    data["nombre"] = data["nombre"].capitalize()
    data["apellido"] = data["apellido"].capitalize()
    data["correo"] = data["correo"].lower()
    data["codigo_RIFD"] = data["codigo_RIFD"].upper()
    data["tipo_usuario"] = data["tipo_usuario"].lower()
    
    

    # Hash the password
    data["contrasena"] = generate_password_hash(data["contrasena"], method='pbkdf2:sha256')

    # Insert user
    users_collection.insert_one(data)
    return jsonify({"message": "Usuario creado exitosamente."}), 201


# Login endpoint
@users_bp.route('/login', methods=['POST'])

def login_user():
    data = request.json

    # Validate input
    if not data or 'rut' not in data or 'contrasena' not in data:
        return jsonify({"error": "RUT y contraseña son requeridos."}), 400

    # Search user by RUT
    user = users_collection.find_one({"rut": data["rut"]})
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    # Check password
    if not check_password_hash(user['contrasena'], data['contrasena']):
        return jsonify({"error": "Contraseña incorrecta."}), 401

    # Create JWT tokens
    access_token = create_access_token(identity=user["rut"])
    refresh_token = create_refresh_token(identity=user["rut"])

    # Success response
    response = jsonify({
        "message": "Login exitoso.",
        "user": {
            "rut": user["rut"],
            "nombre": user["nombre"],
            "apellido": user["apellido"],
            "correo": user["correo"],
            "tipo_usuario": user["tipo_usuario"]
        }
    })
    
    # Set tokens in headers
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.headers["Refresh-Token"] = refresh_token

    return response, 200