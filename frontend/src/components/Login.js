import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [nombre_usuario, setNombreUsuario] = useState('');
  const [contrasenia, setContrasenia] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/usuarios/iniciar-sesion', {
        nombre_usuario,
        contrasenia
      });
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);  // Guardamos el token en el localStorage
        navigate('/home');  // Redirigir al home si el login es exitoso
      }
    } catch (error) {
      console.error('Error en el login', error);
    }
  };

  const goToRegister = () => {
    navigate('/register');  // Redirigir a la página de registro
  };

  return (
    <div className="container">
      <div className="card shadow">
        <div className="card-header text-center bg-primary text-white">
          <h2>Iniciar sesión</h2>
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="nombre_usuario" className="form-label">Nombre de usuario</label>
              <input
                type="text"
                id="nombre_usuario"
                className="form-control"
                placeholder="Ingrese su nombre de usuario"
                value={nombre_usuario}
                onChange={(e) => setNombreUsuario(e.target.value)}
                required
              />
            </div>

            <div className="mb-3">
              <label htmlFor="contrasenia" className="form-label">Contraseña</label>
              <input
                type="password"
                id="contrasenia"
                className="form-control"
                placeholder="Ingrese su contraseña"
                value={contrasenia}
                onChange={(e) => setContrasenia(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary w-100 mb-3">Iniciar sesión</button>
          </form>

          <p className="text-center">
            ¿No tienes una cuenta? <button onClick={goToRegister} className="btn btn-link">Registrarse</button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
