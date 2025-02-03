from app.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

    # Relación con Tareas
    tareas = db.relationship('Tarea', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
