from bson import ObjectId
from . import cartas_bp
from utils.db_utils import get_db
from flask import request, jsonify
from datetime import datetime


db = get_db()
cartas_collection = db['cartas']

# Get all cartas
@cartas_bp.route('/cartas', methods=['GET'])
def get_cartas():
    # Query params
    fecha_inicio = request.args.get("desde") # min date
    fecha_fin = request.args.get("hasta") # max date

    # MongoDB filter
    filtro = {}
    if fecha_inicio or fecha_fin:
        filtro["fecha"] = {}
        if fecha_inicio:
            try:
                # Convert fecha_inicio to datetime object
                filtro["fecha"]["$gte"] = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            except ValueError:
                return jsonify({"message": "El parámetro 'fecha_inicio' debe tener el formato 'YYYY-MM-DD'."}), 400
        if fecha_fin:
            try:
                # Convert fecha_fin to datetime object
                filtro["fecha"]["$lte"] = datetime.strptime(fecha_fin, "%Y-%m-%d")
            except ValueError:
                return jsonify({"message": "El parámetro 'fecha_fin' debe tener el formato 'YYYY-MM-DD'."}), 400

    # MongoDB query
    cartas = list(cartas_collection.find(filtro, {"_id": 0}))

    # Convert datetime objects to string
    for carta in cartas:
        if "fecha" in carta and isinstance(carta["fecha"], datetime):
            carta["fecha"] = carta["fecha"].strftime("%Y-%m-%d")

    return jsonify(cartas), 200

# Get carta by id
@cartas_bp.route('/cartas/<string:id>', methods=['GET'])
def get_carta(id):
    try:
        # Convert id to integer
        id = int(id)
    except ValueError:
        return jsonify({"message": "El ID debe ser un número entero."}), 400

    carta = cartas_collection.find_one({"id": id}, {"_id": 0})
    if not carta:
        return jsonify({"message": "Carta no encontrada."}), 404
    return jsonify(carta), 200


@cartas_bp.route('/cartas', methods=['POST'])
def create_carta():
    required_fields = ["fecha", "alimentos"]  # Required fields
    carta = request.json

    # Check missing fields
    missing_fields = [field for field in required_fields if field not in carta]
    if missing_fields:
        return jsonify({"message": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    # Generate a new numeric ID
    last_carta = cartas_collection.find_one(sort=[("id", -1)])
    new_id = (last_carta["id"] + 1) if last_carta else 1
    carta["id"] = new_id

    # Validate fecha field
    try:
        # Convert fecha to datetime format
        fecha_obj = datetime.strptime(carta["fecha"], "%Y-%m-%d")
        carta["fecha"] = fecha_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        return jsonify({"message": "El campo 'fecha' debe tener el formato 'YYYY-MM-DD'."}), 400

    # Check if a carta already exists for the same date
    existing_carta = cartas_collection.find_one({"fecha": carta["fecha"]})
    if existing_carta:
        return jsonify({"message": f"Ya existe una carta para la fecha {carta['fecha'].strftime('%Y-%m-%d')}."}), 400

    # Validate alimentos field
    if not isinstance(carta["alimentos"], list) or not all(
        "id" in alimento and "nombre" in alimento for alimento in carta["alimentos"]
    ):
        return jsonify({"message": "El campo 'alimentos' debe ser una lista con 'id' y 'nombre' en cada elemento."}), 400

    # Initialize calificaciones field
    carta["calificaciones"] = {"promedio": 0, "total_calificaciones": 0}

    # Try insert carta
    try:
        carta_id = cartas_collection.insert_one(carta).inserted_id
        return jsonify({"message": "Carta creada exitosamente", "_id": str(carta_id)}), 201
    except Exception as e:
        return jsonify({"message": f"Error al crear la carta: {str(e)}"}), 500

# Rate carta
@cartas_bp.route('/cartas/<string:id>/calificar', methods=['POST'])
def calificar_carta(id):
    # Convert id to integer
    try:
        id = int(id)
    except ValueError:
        return jsonify({"message": "El ID debe ser un número válido."}), 400

    calificacion = request.json.get("calificacion")

    # Check rate value between 1 and 5
    if not calificacion or not (1 <= calificacion <= 5):
        return jsonify({"message": "La calificación debe ser un número entre 1 y 5."}), 400

    # Search carta
    carta = cartas_collection.find_one({"id": id})
    if not carta:
        return jsonify({"message": "Carta no encontrada."}), 404

    # Update rate values
    calificaciones = carta.get("calificaciones", {"promedio": 0, "total_calificaciones": 0})
    total_calificaciones = calificaciones["total_calificaciones"] + 1
    suma_calificaciones = calificaciones["promedio"] * calificaciones["total_calificaciones"] + calificacion
    nuevo_promedio = suma_calificaciones / total_calificaciones

    # Save new rate values
    calificaciones["promedio"] = round(nuevo_promedio, 2)  # Round to 2 decimals
    calificaciones["total_calificaciones"] = total_calificaciones

    # Update carta with new rate values
    cartas_collection.update_one(
        {"id": id},
        {"$set": {"calificaciones": calificaciones}}
    )

    return jsonify({"message": "Calificación registrada."}), 200

# Modify carta alimentos
@cartas_bp.route('/cartas/<string:id>/alimentos', methods=['PUT'])
def modify_carta_alimentos(id):
    # Get carta by ID
    carta = cartas_collection.find_one({"id": id})
    if not carta:
        return jsonify({"message": "Carta no encontrada."}), 404

    # Check operation and alimento data
    operation = request.json.get("operation")
    alimento_data = request.json.get("alimento")

    if operation not in ["add", "delete"]:
        return jsonify({"message": "Operación inválida. Usa 'add' o 'delete'."}), 400

    if not alimento_data or "id" not in alimento_data or "nombre" not in alimento_data:
        return jsonify({"message": "Datos del alimento inválidos o faltantes ('id' y 'nombre' son obligatorios)."}), 400

    try:
        if operation == "add":
            # Check if alimento already exists in the list
            if any(a["id"] == alimento_data["id"] for a in carta["alimentos"]):
                return jsonify({"message": "El alimento ya existe en la carta."}), 409

            # Add alimento to the list
            result = cartas_collection.update_one(
                {"id": id},
                {"$push": {"alimentos": alimento_data}}
            )
            return jsonify({"message": "Alimento agregado exitosamente."}), 200

        elif operation == "delete":
            # Check if alimento in list
            if not any(a["id"] == alimento_data["id"] for a in carta["alimentos"]):
                return jsonify({"message": "El alimento no existe en la carta."}), 404

            # Delete alimento from list
            result = cartas_collection.update_one(
                {"id": id},
                {"$pull": {"alimentos": {"id": alimento_data["id"]}}}
            )
            return jsonify({"message": "Alimento eliminado exitosamente."}), 200

    except Exception as e:
        return jsonify({"message": f"Error al modificar los alimentos: {str(e)}."}), 500
