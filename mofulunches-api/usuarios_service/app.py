import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv 
from blueprints.users import users_bp
from config import Config


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_password")  
    jwt = JWTManager(app) 

    
    app.register_blueprint(users_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003, debug=True)
