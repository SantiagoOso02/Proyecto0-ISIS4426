from app.routes.usuario_routes import usuario_bp
from app.routes.tarea_routes import tarea_bp
from app.routes.categoria_routes import categoria_bp

def register_routes(app):
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(tarea_bp, url_prefix='/api/tareas')
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
