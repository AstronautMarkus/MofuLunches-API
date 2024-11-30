from flask import Blueprint

cartas_bp = Blueprint('cartas', __name__)

from . import cartas_routes
