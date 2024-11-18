from flask import Flask
from blueprints.users import users_bp  
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    app.register_blueprint(users_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
