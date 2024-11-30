from flask import Blueprint


alimentos_bp = Blueprint('users', __name__)


from . import alimentos_routes
