from flask import Blueprint

pedidos_bp = Blueprint('cartas', __name__)

from . import pedidos_routes
