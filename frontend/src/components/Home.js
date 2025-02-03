import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';
import '../home.css';

function Home() {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState(null);
  const [tareas, setTareas] = useState([]);
  const [textoTarea, setTextoTarea] = useState('');
  const [estadoTarea, setEstadoTarea] = useState('Sin empezar');
  const [categoriaTarea, setCategoriaTarea] = useState('');
  const [fechaTentativa, setFechaTentativa] = useState('');
  const [categorias, setCategorias] = useState([]);

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    } else {
      const fetchUserData = async () => {
        try {
          const response = await axios.get('http://localhost:5000/api/usuarios/perfil', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          setUsuario(response.data);
        } catch (error) {
          console.error('Error al obtener el perfil del usuario', error);
          navigate('/login');
        }
      };

      fetchUserData();
    }

    // Obtener tareas del usuario autenticado
    const fetchTasks = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/usuarios/tareas', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setTareas(response.data);
      } catch (error) {
        console.error('Error al obtener tareas', error);
      }
    };

    fetchTasks();

    // Obtener categorías
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/categorias/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setCategorias(response.data);
      } catch (error) {
        console.error('Error al obtener categorías', error);
      }
    };

    fetchCategories();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const goToCategories = () => {
    navigate('/categorias');
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    const data = {
      texto: textoTarea,
      estado: estadoTarea,
      id_categoria: categoriaTarea,
      fecha_tentativa_finalizacion: fechaTentativa || null,
    };

    try {
      const response = await axios.post('http://localhost:5000/api/tareas/', data, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 201) {
        setTareas([  // Agregar tarea nueva
          ...tareas,
          {
            ...data,
            id: response.data.id,
            fecha_creacion: format(new Date(), 'yyyy-MM-dd HH:mm:ss'),
            fecha_tentativa_finalizacion: fechaTentativa ? format(new Date(fechaTentativa), 'yyyy-MM-dd') : null,
          },
        ]);
        setTextoTarea('');
        setEstadoTarea('Sin empezar');
        setCategoriaTarea('');
        setFechaTentativa('');
      }
    } catch (error) {
      console.error('Error al crear tarea', error);
    }
  };

  const handleUpdateTask = async (id, newEstado) => {
    try {
      const response = await axios.put(`http://localhost:5000/api/tareas/${id}`, { estado: newEstado }, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        setTareas(tareas.map((tarea) => tarea.id === id ? { ...tarea, estado: newEstado } : tarea));
      }
    } catch (error) {
      console.error('Error al actualizar tarea', error);
    }
  };

  const handleDeleteTask = async (id) => {
    // Eliminar de inmediato del frontend
    setTareas(tareas.filter((tarea) => tarea.id !== id));

    try {
      const response = await axios.delete(`http://localhost:5000/api/tareas/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status !== 200) {
      }
    } catch (error) {
      console.error('Error al eliminar tarea', error);
    }
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <h2>Bienvenido {usuario ? usuario.nombre_usuario : ''}</h2>
        <div className="profile-container">
          {usuario && (
            <img
              src={`http://localhost:5000/${usuario.imagen_perfil}`}
              alt="Perfil"
              className="profile-img"
            />
          )}
          <button onClick={handleLogout} className="logout-btn">Cerrar sesión</button>
        </div>
      </header>

      <div className="category-button-container">
        <button onClick={goToCategories} className="category-btn">Ir a Categorías</button>
      </div>

      <div className="task-form-container">
        <h3>Crear nueva tarea</h3>
        <form onSubmit={handleCreateTask} className="task-form">
          <input
            type="text"
            placeholder="Texto de la tarea"
            value={textoTarea}
            onChange={(e) => setTextoTarea(e.target.value)}
            className="input-field"
            required
          />
          <select
            value={categoriaTarea}
            onChange={(e) => setCategoriaTarea(e.target.value)}
            className="input-field"
            required
          >
            <option value="">Seleccionar categoría</option>
            {categorias.map((categoria) => (
              <option key={categoria.id} value={categoria.id}>
                {categoria.nombre}
              </option>
            ))}
          </select>
          <select
            value={estadoTarea}
            onChange={(e) => setEstadoTarea(e.target.value)}
            className="input-field"
            required
          >
            <option value="Sin empezar">Sin empezar</option>
            <option value="Empezada">Empezada</option>
            <option value="Finalizada">Finalizada</option>
          </select>
          <input
            type="date"
            placeholder="Fecha tentativa de finalización"
            value={fechaTentativa}
            onChange={(e) => setFechaTentativa(e.target.value)}
            className="input-field"
          />
          <button type="submit" className="submit-btn">Crear tarea</button>
        </form>
      </div>

      <div className="task-list-container">
        <h3>Listado de tareas</h3>
        <table className="task-table">
          <thead>
            <tr>
              <th>Texto</th>
              <th>Estado</th>
              <th>Fecha de creación</th>
              <th>Fecha tentativa</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {tareas.length > 0 ? (
              tareas.map((tarea) => (
                <tr key={tarea.id}>
                  <td>{tarea.texto}</td>
                  <td>
                    <select
                      value={tarea.estado}
                      onChange={(e) => handleUpdateTask(tarea.id, e.target.value)}
                      className="task-status-select"
                    >
                      <option value="Sin empezar">Sin empezar</option>
                      <option value="Empezada">Empezada</option>
                      <option value="Finalizada">Finalizada</option>
                    </select>
                  </td>
                  <td>{format(new Date(tarea.fecha_creacion), 'dd/MM/yyyy HH:mm:ss')}</td>
                  <td>{tarea.fecha_tentativa_finalizacion ? format(new Date(tarea.fecha_tentativa_finalizacion), 'dd/MM/yyyy') : ''}</td>
                  <td>
                    <button
                      onClick={() => handleDeleteTask(tarea.id)}
                      className="delete-btn"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">No hay tareas disponibles.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Home;
