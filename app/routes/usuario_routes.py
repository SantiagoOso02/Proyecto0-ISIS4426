from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService
from app.services.tarea_service import TareaService
from flask_jwt_extended import jwt_required, get_jwt_identity

usuario_bp = Blueprint('usuarios', __name__)

# Iniciar sesión
@usuario_bp.route('/iniciar-sesion', methods=['POST'])
def iniciar_sesion():
    data = request.json
    token = UsuarioService.iniciar_sesion(data.get('nombre_usuario'), data.get('contrasenia'))

    if not token:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    return jsonify({"mensaje": "Inicio de sesión exitoso", "token": token}), 200

# Obtener el perfil del usuario autenticado
@usuario_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil():
    usuario_id = int(get_jwt_identity())  # Convertimos el ID a entero
    usuario = UsuarioService.obtener_usuario_por_id(usuario_id)

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "imagen_perfil": usuario.imagen_perfil
    }), 200


# Obtener la lista de tareas de un usuario
@usuario_bp.route('/tareas', methods=['GET'])
@jwt_required()
def obtener_tareas_por_usuario():
    # Obtener el ID del usuario desde el token JWT
    id_usuario = get_jwt_identity()

    # Filtrar las tareas por el id_usuario
    tareas = TareaService.obtener_tareas_por_usuario(id_usuario)

    if not tareas:
        return jsonify({'mensaje': 'No se encontraron tareas para este usuario'}), 404

    return jsonify([{
        'id': tarea.id,
        'texto': tarea.texto,
        'fecha_creacion': tarea.fecha_creacion.isoformat(),
        'fecha_tentativa_finalizacion': tarea.fecha_tentativa_finalizacion.isoformat() if tarea.fecha_tentativa_finalizacion else None,
        'estado': tarea.estado,
        'id_usuario': tarea.id_usuario,
        'id_categoria': tarea.id_categoria
    } for tarea in tareas]), 200


# Crear un nuevo usuario
@usuario_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.form  # Captura los datos como formulario
    imagen = request.files.get('imagen')  # Obtiene la imagen si se envía

    usuario = UsuarioService.crear_usuario(data, imagen)

    if not usuario:
        return jsonify({"mensaje": "El nombre de usuario ya está en uso"}), 400

    return jsonify({
        "mensaje": "Usuario creado exitosamente",
        "id": usuario.id,
        "imagen_perfil": usuario.imagen_perfil
    }), 201

# Obtener todos los usuarios
@usuario_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_todos():
    usuarios = UsuarioService.obtener_todos()
    return jsonify([{
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "imagen_perfil": usuario.imagen_perfil
    } for usuario in usuarios]), 200

# Obtener un usuario por ID
@usuario_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_por_id(id):
    usuario = UsuarioService.obtener_usuario_por_id(id)

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "imagen_perfil": usuario.imagen_perfil
    }), 200

# Actualizar un usuario
@usuario_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_usuario(id):
    data = request.json
    usuario = UsuarioService.actualizar_usuario(id, data)

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200

# Eliminar un usuario
@usuario_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(id):
    eliminado = UsuarioService.eliminar_usuario(id)

    if not eliminado:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 204
