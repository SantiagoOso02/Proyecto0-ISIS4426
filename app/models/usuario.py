from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)
    imagen_perfil = db.Column(db.String(255), nullable=False, default='./uploads/default_profile.png')  # Imagen por defecto

    # Relación con Tareas
    tareas = db.relationship('Tarea', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'
