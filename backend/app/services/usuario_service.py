import os
from app.models.usuario import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token

UPLOAD_FOLDER = 'uploads/'  # Carpeta donde se guardarán las imágenes


class UsuarioService:

    @staticmethod
    def iniciar_sesion(nombre_usuario, contrasenia):
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if not usuario or not check_password_hash(usuario.contrasenia, contrasenia):
            return None  # Indica que la autenticación falló
        return create_access_token(identity=str(usuario.id))  # Retorna el token JWT

    @staticmethod
    def obtener_usuario_por_id(id):
        return Usuario.query.get(id)
    @staticmethod
    def crear_usuario(data, imagen):
        if Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first():
            return None  # Usuario ya existe

        # Si se sube una imagen, guardarla en el servidor
        if imagen:
            filename = secure_filename(imagen.filename)
            ruta_imagen = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(ruta_imagen)
        else:
            ruta_imagen = 'uploads/default_profile.png'  # Imagen por defecto

        usuario = Usuario(
            nombre_usuario=data['nombre_usuario'],
            contrasenia=generate_password_hash(data['contrasenia']),
            imagen_perfil=ruta_imagen
        )

        db.session.add(usuario)
        db.session.commit()
        return usuario
    @staticmethod
    def obtener_todos():
        return Usuario.query.all()

    @staticmethod
    def actualizar_usuario(id, data):
        usuario = Usuario.query.get(id)
        if not usuario:
            return None  # Indica que el usuario no existe

        usuario.nombre_usuario = data.get('nombre_usuario', usuario.nombre_usuario)
        if 'contrasenia' in data:
            usuario.contrasenia = generate_password_hash(data['contrasenia'])
        usuario.imagen_perfil = data.get('imagen_perfil', usuario.imagen_perfil)

        db.session.commit()
        return usuario

    @staticmethod
    def eliminar_usuario(id):
        usuario = Usuario.query.get(id)
        if not usuario:
            return False  # Indica que el usuario no existe

        db.session.delete(usuario)
        db.session.commit()
        return True  # Indica éxito en la eliminación
