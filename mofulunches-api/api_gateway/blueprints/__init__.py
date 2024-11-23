from .alimentos_service.alimentos import alimentos_bp
from .pedidos_service.pedidos import pedidos_bp
from .usuarios_service.usuarios import usuarios_bp

def register_blueprints(app):
    app.register_blueprint(alimentos_bp, url_prefix='/alimentos')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
