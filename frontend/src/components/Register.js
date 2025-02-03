import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [nombre_usuario, setNombreUsuario] = useState('');
  const [contrasenia, setContrasenia] = useState('');
  const [imagen, setImagen] = useState(null);
  const [error, setError] = useState(''); // Estado para manejar errores
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('nombre_usuario', nombre_usuario);
    formData.append('contrasenia', contrasenia);
    if (imagen) {
      formData.append('imagen', imagen);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/usuarios', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      if (response.data.mensaje === "Usuario creado exitosamente") {
        navigate('/login');  // Redirigir a login después de registrarse
      } else {
        setError(response.data.mensaje || 'Error desconocido');
      }
    } catch (error) {
      // Verifica si el error tiene una respuesta y maneja el mensaje de error
      if (error.response) {
        setError(error.response.data.mensaje || 'Error en el registro');
      } else {
        setError('No se pudo conectar con el servidor');
      }
      console.error('Error en el registro', error);
    }
  };

  const goToLogin = () => {
    navigate('/login');  // Redirigir a la página de login
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header text-center">
              <h3>Registro</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="nombre_usuario" className="form-label">Nombre de usuario</label>
                  <input
                    type="text"
                    className="form-control"
                    id="nombre_usuario"
                    placeholder="Nombre de usuario"
                    value={nombre_usuario}
                    onChange={(e) => setNombreUsuario(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="contrasenia" className="form-label">Contraseña</label>
                  <input
                    type="password"
                    className="form-control"
                    id="contrasenia"
                    placeholder="Contraseña"
                    value={contrasenia}
                    onChange={(e) => setContrasenia(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="imagen" className="form-label">Imagen de perfil (opcional)</label>
                  <input
                    type="file"
                    className="form-control"
                    id="imagen"
                    onChange={(e) => setImagen(e.target.files[0])}
                  />
                </div>
                {error && <div className="alert alert-danger">{error}</div>}
                <button type="submit" className="btn btn-primary w-100">Registrar</button>
              </form>
              <div className="mt-3 text-center">
                <p>¿Ya tienes cuenta? <button onClick={goToLogin} className="btn btn-link">Iniciar sesión</button></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
