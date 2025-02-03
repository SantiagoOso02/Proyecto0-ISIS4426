import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CategoryPage() {
  const [categorias, setCategorias] = useState([]);
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const navigate = useNavigate();

  // Obtener todas las categorías al cargar el componente
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/categorias/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setCategorias(response.data);
      } catch (error) {
        console.error('Error al obtener las categorías', error);
      }
    };

    fetchCategories();
  }, []);

  // Manejar el envío del formulario de creación
  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = { nombre, descripcion };

    try {
      const response = await axios.post('http://localhost:5000/api/categorias/', data, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 201) {
        // Una vez que la categoría sea creada, recargar las categorías
        setCategorias([...categorias, { id: response.data.id, nombre, descripcion }]);
        setNombre(''); // Limpiar el formulario
        setDescripcion('');
      }
    } catch (error) {
      console.error('Error al crear la categoría', error);
    }
  };

  // Redirigir a la página de inicio
  const goToHome = () => {
    navigate('/home'); // Redirige a la página de inicio
  };

  return (
    <div className="container">
      <h2>Categorías</h2>

      {/* Botón para ir a la página de inicio */}
      <button onClick={goToHome} className="btn btn-primary mb-4">
        Ir a Home
      </button>

      {/* Listado de categorías como tabla */}
      <div className="my-4">
        <h3>Listado de Categorías</h3>
        {categorias.length > 0 ? (
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
              </tr>
            </thead>
            <tbody>
              {categorias.map((categoria) => (
                <tr key={categoria.id}>
                  <td>{categoria.nombre}</td>
                  <td>{categoria.descripcion}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No hay categorías disponibles.</p>
        )}
      </div>

      {/* Formulario para crear categoría */}
      <div>
        <h3>Crear Nueva Categoría</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Nombre de la categoría"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Descripción"
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-success">
            Crear Categoría
          </button>
        </form>
      </div>
    </div>
  );
}

export default CategoryPage;
