from flask import Blueprint


users_bp = Blueprint('users', __name__)


from . import usuarios_routes
