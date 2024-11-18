from flask import request, jsonify
from . import users_bp
from utils.db_utils import get_db


db = get_db()
users_collection = db['usuarios']

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # no id
    return jsonify(users), 200

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Invalid data"}), 400
    users_collection.insert_one(data)
    return jsonify({"message": "User created"}), 201
