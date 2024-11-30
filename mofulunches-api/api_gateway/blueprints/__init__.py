from .alimentos_service.alimentos import create_alimentos_blueprint
from .pedidos_service.pedidos import create_pedidos_blueprint
from .usuarios_service.usuarios import create_usuarios_blueprint

def register_blueprints(app):
    app.register_blueprint(create_usuarios_blueprint(), url_prefix='/api')
    app.register_blueprint(create_pedidos_blueprint(), url_prefix='/api')
    app.register_blueprint(create_alimentos_blueprint(), url_prefix='/api')
