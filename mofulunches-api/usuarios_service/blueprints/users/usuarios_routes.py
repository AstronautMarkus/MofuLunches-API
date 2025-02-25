from . import users_bp
from utils.db_utils import get_db
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash


class UsersCollection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsersCollection, cls).__new__(cls)
            db = get_db()
            cls._instance.collection = db['usuarios']
        return cls._instance


users_collection = UsersCollection().collection

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


# Update user full data
@users_bp.route('/usuarios/<rut>', methods=['PUT'])
def update_user(rut):
    data = request.json

    required_fields = ["apellido", "codigo_RFID", "correo", "nombre", "rut", "tipo_usuario"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": "Faltan campos obligatorios.", "missing_fields": missing_fields}), 400

    normalized_data = {
        "nombre": data["nombre"].capitalize(),
        "apellido": data["apellido"].capitalize(),
        "correo": data["correo"].lower(),
        "codigo_RFID": data["codigo_RFID"].upper(),
        "tipo_usuario": data["tipo_usuario"].lower(),
        "rut": rut
    }

    result = users_collection.update_one({"rut": rut}, {"$set": normalized_data})
    
    if result.matched_count:
        return jsonify({"message": "Usuario actualizado exitosamente."}), 200
    return jsonify({"error": "Usuario no encontrado."}), 404


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

    required_fields = ["rut", "nombre", "apellido", "correo", "contrasena", "tipo_usuario"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Verify RUT is an integer and has valid length
    try:
        int(data["rut"])
        if not (8 <= len(data["rut"]) <= 9):
            return jsonify({"error": "El RUT debe tener entre 8 y 9 caracteres."}), 400
    except ValueError:
        return jsonify({"error": "El campo RUT solo debe contener números."}), 400

    if users_collection.find_one({"rut": data["rut"]}):
        return jsonify({"error": "El RUT ya existe."}), 400

    # Validate tipo_usuario
    valid_user_types = ["cocineros", "admin", "empleado"]
    if data["tipo_usuario"].lower() not in valid_user_types:
        return jsonify({"error": f"Tipo de usuario inválido. Debe ser uno de los siguientes: {', '.join(valid_user_types)}"}), 400

    data["nombre"] = data["nombre"].capitalize()
    data["apellido"] = data["apellido"].capitalize()
    data["correo"] = data["correo"].lower()
    data["codigo_RFID"] = data.get("codigo_RFID", "NO_ASIGNADO").upper()
    data["tipo_usuario"] = data["tipo_usuario"].lower()
    data["contrasena"] = generate_password_hash(data["contrasena"], method='pbkdf2:sha256')

    users_collection.insert_one(data)
    return jsonify({"message": "Usuario creado exitosamente."}), 201


# Update user partial data
@users_bp.route('/usuarios/<rut>', methods=['PATCH'])
def edit_user(rut):
    data = request.json
    result = users_collection.update_one({"rut": rut}, {"$set": data})

    if result.matched_count:
        return jsonify({"message": "Usuario actualizado exitosamente."}), 200
    return jsonify({"error": "Usuario no encontrado."}), 404


# Login endpoint
@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json

    if not data or 'rut' not in data or 'contrasena' not in data:
        return jsonify({"error": "RUT y contraseña son requeridos."}), 400

    user = users_collection.find_one({"rut": data["rut"]})
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    if not check_password_hash(user['contrasena'], data['contrasena']):
        return jsonify({"error": "Contraseña incorrecta."}), 401

    access_token = create_access_token(identity=user["rut"])
    refresh_token = create_refresh_token(identity=user["rut"])

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
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.headers["Refresh-Token"] = refresh_token

    return response, 200
