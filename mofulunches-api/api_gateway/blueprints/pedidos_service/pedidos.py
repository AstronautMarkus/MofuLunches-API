from flask import Blueprint, jsonify, current_app
import requests

pedidos_bp = Blueprint('pedidos', __name__)

