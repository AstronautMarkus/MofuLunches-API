from bson import ObjectId
from . import pedidos_bp
from utils.db_utils import get_db
from flask import request, jsonify


db = get_db()
pedidos_collection = db['pedidos']

# Get all pedidos
@pedidos_bp.route('/pedidos', methods=['GET'])
def get_cartas():
    pedidos = list(pedidos_collection.find({}, {"_id": 0}))  # exclude _id field
    return jsonify(pedidos), 200

