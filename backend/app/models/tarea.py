from app.extensions import db
from datetime import datetime

class Tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_tentativa_finalizacion = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='Sin Empezar')

    # Claves foráneas
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    def __repr__(self):
        return f'<Tarea {self.texto}>'
