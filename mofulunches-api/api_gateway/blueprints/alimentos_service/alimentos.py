from flask import Blueprint, jsonify, current_app
import requests

alimentos_bp = Blueprint('alimentos', __name__)
