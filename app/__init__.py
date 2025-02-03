import os
from flask import Flask, send_from_directory
from app.extensions import db, jwt
from app.config import Config
from app.routes import register_routes
from flask_cors import CORS


def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar carpeta de subida de imágenes
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Crea la carpeta si no existe
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

   # Configurar CORS para permitir solicitudes de cualquier origen (o especificar los permitidos)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Inicializar la base de datos con la aplicación
    db.init_app(app)
    jwt.init_app(app)  # Vincula el JWTManager a la aplicación Flask

    # Registrar rutas
    register_routes(app)

    # Endpoint para servir archivos de la carpeta 'uploads/'
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
