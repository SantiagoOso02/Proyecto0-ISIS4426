from flask import Blueprint, request, jsonify
from app.services.categoria_service import CategoriaService
from flask_jwt_extended import jwt_required

categoria_bp = Blueprint('categorias', __name__)

# Obtener todas las categorías
@categoria_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_categorias():
    categorias = CategoriaService.obtener_todas()
    return jsonify([{
        'id': cat.id,
        'nombre': cat.nombre,
        'descripcion': cat.descripcion
    } for cat in categorias]), 200

# Obtener una categoría por ID
@categoria_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_categoria(id):
    categoria = CategoriaService.obtener_por_id(id)
    if not categoria:
        return jsonify({'mensaje': 'Categoría no encontrada'}), 404

    return jsonify({
        'id': categoria.id,
        'nombre': categoria.nombre,
        'descripcion': categoria.descripcion
    }), 200

# Crear una nueva categoría
@categoria_bp.route('/', methods=['POST'])
@jwt_required()
def crear_categoria():
    data = request.get_json()
    categoria = CategoriaService.crear_categoria(data)

    if not categoria:
        return jsonify({'mensaje': 'El nombre de la categoría ya está en uso'}), 400

    return jsonify({'mensaje': 'Categoría creada exitosamente', 'id': categoria.id}), 201

# Actualizar una categoría
@categoria_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_categoria(id):
    data = request.get_json()
    categoria = CategoriaService.actualizar_categoria(id, data)

    if not categoria:
        return jsonify({'mensaje': 'Categoría no encontrada'}), 404

    return jsonify({'mensaje': 'Categoría actualizada exitosamente'}), 200

# Eliminar una categoría
@categoria_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_categoria(id):
    eliminado = CategoriaService.eliminar_categoria(id)

    if not eliminado:
        return jsonify({'mensaje': 'Categoría no encontrada'}), 404

    return jsonify({'mensaje': 'Categoría eliminada exitosamente'}), 204
