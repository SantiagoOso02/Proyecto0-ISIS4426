from app.models.categoria import Categoria
from app.extensions import db

class CategoriaService:

    @staticmethod
    def obtener_todas():
        return Categoria.query.all()

    @staticmethod
    def obtener_por_id(id):
        return Categoria.query.get(id)

    @staticmethod
    def crear_categoria(data):
        if Categoria.query.filter_by(nombre=data['nombre']).first():
            return None  # Indica que la categoría ya existe

        nueva_categoria = Categoria(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', '')
        )

        db.session.add(nueva_categoria)
        db.session.commit()
        return nueva_categoria

    @staticmethod
    def actualizar_categoria(id, data):
        categoria = Categoria.query.get(id)
        if not categoria:
            return None  # Indica que la categoría no existe

        categoria.nombre = data.get('nombre', categoria.nombre)
        categoria.descripcion = data.get('descripcion', categoria.descripcion)

        db.session.commit()
        return categoria

    @staticmethod
    def eliminar_categoria(id):
        categoria = Categoria.query.get(id)
        if not categoria:
            return False  # Indica que la categoría no existe

        db.session.delete(categoria)
        db.session.commit()
        return True  # Indica éxito en la eliminación
