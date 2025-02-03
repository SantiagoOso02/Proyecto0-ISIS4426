from flask import Blueprint, request, jsonify
from app.services.tarea_service import TareaService
from flask_jwt_extended import jwt_required

tarea_bp = Blueprint('tareas', __name__)

# Obtener todas las tareas
@tarea_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_tareas():
    tareas = TareaService.obtener_todas()
    return jsonify([{
        'id': tarea.id,
        'texto': tarea.texto,
        'fecha_creacion': tarea.fecha_creacion.isoformat(),
        'fecha_tentativa_finalizacion': tarea.fecha_tentativa_finalizacion.isoformat() if tarea.fecha_tentativa_finalizacion else None,
        'estado': tarea.estado,
        'id_usuario': tarea.id_usuario,
        'id_categoria': tarea.id_categoria
    } for tarea in tareas]), 200

# Obtener una tarea por ID
@tarea_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_tarea(id):
    tarea = TareaService.obtener_por_id(id)
    if not tarea:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404

    return jsonify({
        'id': tarea.id,
        'texto': tarea.texto,
        'fecha_creacion': tarea.fecha_creacion.isoformat(),
        'fecha_tentativa_finalizacion': tarea.fecha_tentativa_finalizacion.isoformat() if tarea.fecha_tentativa_finalizacion else None,
        'estado': tarea.estado,
        'id_usuario': tarea.id_usuario,
        'id_categoria': tarea.id_categoria
    }), 200

@tarea_bp.route('/', methods=['POST'])
@jwt_required()
def crear_tarea():
    data = request.get_json()
    tarea = TareaService.crear_tarea(data)

    # Si la función devuelve una tupla, es un error (mensaje, código HTTP)
    if isinstance(tarea, tuple):
        return jsonify(tarea[0]), tarea[1]

    return jsonify({'mensaje': 'Tarea creada exitosamente', 'id': tarea.id}), 201
# Actualizar una tarea
@tarea_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_tarea(id):
    data = request.get_json()
    tarea = TareaService.actualizar_tarea(id, data)

    if not tarea:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404

    return jsonify({'mensaje': 'Tarea actualizada exitosamente'}), 200

# Eliminar una tarea
@tarea_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_tarea(id):
    eliminado = TareaService.eliminar_tarea(id)

    if not eliminado:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404

    return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 204
