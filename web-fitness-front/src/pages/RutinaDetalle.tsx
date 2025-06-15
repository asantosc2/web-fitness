import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
  tipo_equipo: string;
  descripcion?: string;
}

interface EjercicioDeRutina {
  id: number;
  ejercicio_id: number;
  orden: number;
  series: number;
  repeticiones: number;
  comentarios?: string;
  ejercicio: Ejercicio;
}

interface Rutina {
  id: number;
  nombre: string;
  descripcion?: string;
  es_defecto: boolean;
  usuario_id?: number;
}

export default function RutinaDetalle() {
  const { id } = useParams();
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [ejercicios, setEjercicios] = useState<EjercicioDeRutina[]>([]);
  const [rutina, setRutina] = useState<Rutina | null>(null);
  const [seriesPorEjercicio, setSeriesPorEjercicio] = useState<{ [key: number]: number }>({});

  useEffect(() => {
    fetch(`http://localhost:8000/rutinas/${id}`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then(res => res.json())
      .then(data => setRutina(data))
      .catch(err => console.error("Error al cargar rutina:", err));
  }, [id, estado.token]);

  useEffect(() => {
    fetch(`http://localhost:8000/rutinas/${id}/ejercicios`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then(res => res.json())
      .then(data => {
        setEjercicios(data);
        data.forEach((ej: EjercicioDeRutina) => {
          fetch(`http://localhost:8000/rutina-ejercicio/${ej.id}/series`, {
            headers: { Authorization: `Bearer ${estado.token}` },
          })
            .then(res => res.json())
            .then(series => {
              setSeriesPorEjercicio(prev => ({ ...prev, [ej.id]: series.length }));
            });
        });
      })
      .catch(err => console.error("Error al cargar ejercicios:", err));
  }, [id, estado.token]);

  const iniciarSesion = async () => {
    try {
      const res = await fetch("http://localhost:8000/sesiones", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify({
          rutina_id: Number(id),
          nota: "Sesión generada desde la rutina",
        }),
      });

      if (!res.ok) {
        const error = await res.json();
        alert(error.detail || "Error al iniciar sesión");
        return;
      }

      const sesion = await res.json();
      navigate(`/sesiones/${sesion.id}`);
    } catch (err) {
      console.error("Error al crear sesión:", err);
      alert("Error inesperado al iniciar sesión");
    }
  };

  const copiarRutina = async () => {
    try {
      const res = await fetch(`http://localhost:8000/rutinas/${id}/copiar`, {
        method: "POST",
        headers: { Authorization: `Bearer ${estado.token}` },
      });

      if (!res.ok) {
        const error = await res.json();
        alert(error.detail || "Error al copiar rutina");
        return;
      }

      const nueva = await res.json();
      alert("Rutina copiada con éxito");
      navigate(`/rutinas/${nueva.id}`);
    } catch (err) {
      console.error("Error al copiar rutina:", err);
      alert("Error inesperado");
    }
  };

  const eliminarRutina = async () => {
    const confirmacion = window.confirm("¿Seguro que quieres eliminar esta rutina?");
    if (!confirmacion) return;

    try {
      const res = await fetch(`http://localhost:8000/rutinas/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${estado.token}` },
      });

      if (!res.ok) {
        const error = await res.json();
        alert(error.detail || "Error al eliminar rutina");
        return;
      }

      alert("Rutina eliminada con éxito");
      navigate("/rutinas");
    } catch (err) {
      console.error("Error al eliminar rutina:", err);
      alert("Error inesperado");
    }
  };

  const editarRutina = () => {
    navigate(`/rutinas/${rutina?.id}/editar`);
  };

  if (!id || !rutina) {
    return (
      <div className="text-center mt-20 text-gray-500">
        Cargando rutina...
      </div>
    );
  }

  return (

    <div className="min-h-screen bg-gray-100 pt-24 px-6">

      <Navbar />
      <div className="max-w-3xl mx-auto">
        {/* 🔙 Botón para volver atrás */}
        <div className="mb-4">
          <button
            onClick={() => navigate(-1)}
            className="text-blue-600 hover:underline"
          >
            ⬅ Volver atrás
          </button>
        </div>
        <h1 className="text-3xl font-bold text-blue-600 mb-2 text-center">
          {rutina.nombre}
        </h1>
        {rutina.descripcion && (
          <p className="text-center text-gray-600 mb-6">{rutina.descripcion}</p>
        )}

        {ejercicios.length === 0 ? (
          <p className="text-center text-gray-600">Esta rutina aún no tiene ejercicios.</p>
        ) : (
          <ul className="space-y-4">
            {ejercicios.map(e => (
              <li key={e.id} className="bg-white shadow p-4 rounded">
                <p className="font-semibold text-lg">
                  {seriesPorEjercicio[e.id] ?? 0} × {e.ejercicio.nombre}
                </p>
                <p className="text-sm text-gray-600">{e.ejercicio.grupo_muscular}</p>
              </li>
            ))}
          </ul>
        )}

        <div className="mt-8 text-center space-x-4">
          {rutina.es_defecto ? (
            <button
              onClick={copiarRutina}
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 shadow"
            >
              Copiar rutina a tus plantillas
            </button>
          ) : (
            <>
              <button
                onClick={iniciarSesion}
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 shadow"
              >
                Iniciar esta rutina como sesión
              </button>
              <button
                onClick={eliminarRutina}
                className="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700 shadow"
              >
                Eliminar rutina
              </button>
              {rutina.usuario_id === estado.usuario?.id && (
                <button
                  onClick={editarRutina}
                  className="bg-yellow-500 text-white px-6 py-2 rounded hover:bg-yellow-600 shadow"
                >
                  Editar rutina
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
