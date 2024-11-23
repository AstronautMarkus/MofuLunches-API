from flask import Flask, render_template
import requests

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    @app.route('/status', methods=['GET'])
    def check_services_status():
        services = {
            'alimentos_service': app.config['ALIMENTOS_SERVICE_URL'],
            'pedidos_service': app.config['PEDIDOS_SERVICE_URL'],
            'usuarios_service': app.config['USUARIOS_SERVICE_URL']
        }
        
        statuses = {}
        
        for service_name, service_url in services.items():
            try:
                # Ping to service
                response = requests.get(service_url, timeout=2)
                statuses[service_name] = {'status': 'Online', 'url': service_url}
            except requests.exceptions.RequestException:
                # If service is not available, store status as Offline
                statuses[service_name] = {'status': 'Offline', 'url': service_url}
  
        return render_template('status.html', statuses=statuses)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
