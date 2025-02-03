from app.models.tarea import Tarea
from app.extensions import db
from datetime import datetime

class TareaService:

    @staticmethod
    def obtener_tareas_por_usuario(id_usuario):
        return Tarea.query.filter_by(id_usuario=id_usuario).all()

    @staticmethod
    def obtener_todas():
        return Tarea.query.all()

    @staticmethod
    def obtener_por_id(id):
        return Tarea.query.get(id)

    @staticmethod
    def crear_tarea(data):
        # Obtener la fecha tentativa si está presente
        fecha_tentativa = data.get('fecha_tentativa_finalizacion')
        
        # Verificar si la fecha tentativa es válida
        if fecha_tentativa:
            try:
                # Intentar convertir la fecha a datetime
                fecha_tentativa = datetime.fromisoformat(fecha_tentativa)
                # Verificar si la fecha tentativa es anterior a la fecha actual
                if fecha_tentativa < datetime.utcnow():
                    return {"error": "La fecha tentativa no puede ser anterior a la fecha actual"}, 400
            except ValueError:
                # Si la conversión falla, devolver un error
                return {"error": "Formato de fecha tentativa no válido"}, 400

        # Crear la nueva tarea
        nueva_tarea = Tarea(
            texto=data['texto'],
            fecha_creacion=datetime.utcnow(),
            fecha_tentativa_finalizacion=fecha_tentativa,  # Puede ser None si no se proporcionó
            estado=data.get('estado', 'Sin Empezar'),
            id_usuario=data['id_usuario'],
            id_categoria=data['id_categoria']
        )

        # Agregar la tarea a la base de datos y confirmar el commit
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return nueva_tarea

    @staticmethod
    def actualizar_tarea(id, data):
        tarea = Tarea.query.get(id)
        if not tarea:
            return None  # Indica que la tarea no existe

        # Permitir solo cambios en el texto y el estado
        tarea.texto = data.get('texto', tarea.texto)
        tarea.estado = data.get('estado', tarea.estado)

        db.session.commit()
        return tarea

    @staticmethod
    def eliminar_tarea(id):
        tarea = Tarea.query.get(id)
        if not tarea:
            return False  # Indica que la tarea no existe

        db.session.delete(tarea)
        db.session.commit()
        return True  # Indica éxito en la eliminación
