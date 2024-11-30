import platform
import psutil
from flask import Flask, render_template
import socket
import time
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, OperationFailure
from blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    register_blueprints(app)

    def get_system_info():
        """Server info."""
        boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
        disk_usage = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        system_info = {
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "Python Version": platform.python_version(),
            "CPU Cores": psutil.cpu_count(logical=True),
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
            "Memory Total (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "Memory Available (GB)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
            "System Uptime": boot_time,
        }
        return system_info

    def check_mongodb_status():
        """Verifica el estado de la base de datos MongoDB remota y maneja errores."""
        mongo_uri = app.config['MONGODB_URI']  
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)  
            client.admin.command('ping')  
            return {
                "status": "Online",
                "host": mongo_uri.split('@')[-1], 
                "error": None
            }
        except ConnectionFailure as e:
            return {
                "status": "Offline",
                "host": mongo_uri.split('@')[-1],
                "error": f"Connection Failure: {e}"
            }
        except ConfigurationError as e:
            return {
                "status": "Offline",
                "host": mongo_uri.split('@')[-1],
                "error": f"Configuration Error: {e}"
            }
        except OperationFailure as e:
            return {
                "status": "Offline",
                "host": mongo_uri.split('@')[-1],
                "error": f"Operation Failure: {e}"
            }
        except Exception as e:
            return {
                "status": "Offline",
                "host": mongo_uri.split('@')[-1],
                "error": f"Unexpected Error: {e}"
            }

    def check_world_time_api_status():
        """Verifica el estado de la API de Tiempo Mundial."""
        world_time_api_url = "http://worldtimeapi.org/api/timezone/America/Santiago"
        try:
            response = requests.get(world_time_api_url, timeout=2)
            return {
                "status": "Online",
                "url": world_time_api_url,
                "error": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "Offline",
                "url": world_time_api_url,
                "error": str(e)
            }

    @app.route('/status', methods=['GET'])
    def check_services_status():
        
        services = {
            'alimentos_service': app.config['ALIMENTOS_SERVICE_URL'],
            'pedidos_service': app.config['PEDIDOS_SERVICE_URL'],
            'usuarios_service': app.config['USUARIOS_SERVICE_URL']
        }
        
        
        statuses = {}
        all_systems_operational = True

        for service_name, service_url in services.items():
            try:
                response = requests.get(service_url, timeout=2)
                statuses[service_name] = {'status': 'Online', 'url': service_url, 'error': None}
            except requests.exceptions.RequestException as e:
                statuses[service_name] = {'status': 'Offline', 'url': service_url, 'error': str(e)}
                all_systems_operational = False

        
        mongodb_status = check_mongodb_status()
        if mongodb_status['status'] == "Offline":
            all_systems_operational = False

        # Check World Time API status
        world_time_api_status = check_world_time_api_status()
        if world_time_api_status['status'] == "Offline":
            all_systems_operational = False

        
        system_info = get_system_info()

        
        return render_template(
            'status.html', 
            statuses=statuses, 
            all_systems_operational=all_systems_operational,
            system_info=system_info,
            mongodb_status=mongodb_status,
            world_time_api_status=world_time_api_status
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
