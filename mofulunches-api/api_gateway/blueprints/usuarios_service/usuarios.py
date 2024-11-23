from flask import Blueprint, jsonify, current_app
import requests

usuarios_bp = Blueprint('usuarios', __name__)
