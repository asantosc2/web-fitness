import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { Pencil, Trash, Play, Copy, ArrowLeft } from "lucide-react";
import { toast } from "react-hot-toast";

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
        body: JSON.stringify({ rutina_id: Number(id) }),
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
      toast.success("Rutina copiada con éxito");
      navigate(`/rutinas/${nueva.id}`);
    } catch (err) {
      console.error("Error al copiar rutina:", err);
      toast.error("Error inesperado");
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

      toast.success("Rutina eliminada con éxito");
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
    return <div className="text-center mt-20 text-gray-500">Cargando rutina...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto">
        {/* Volver */}
        <button
          onClick={() => navigate(-1)}
          className="text-orange-600 hover:underline mb-6 flex items-center gap-1"
        >
          <ArrowLeft size={18} /> Volver
        </button>

        <h1 className="text-4xl font-bold text-orange-700 text-center mb-2">
          {rutina.nombre}
        </h1>
        {rutina.descripcion && (
          <p className="text-center text-gray-600 mb-8">{rutina.descripcion}</p>
        )}

        {/* Lista de ejercicios */}
        {ejercicios.length === 0 ? (
          <p className="text-center text-gray-600">Esta rutina aún no tiene ejercicios.</p>
        ) : (
          <ul className="space-y-4">
            {ejercicios.map(e => (
              <li key={e.id} className="bg-white shadow-md p-4 rounded-lg">
                <p className="text-lg font-semibold text-gray-800">
                  {seriesPorEjercicio[e.id] ?? 0} × {e.ejercicio.nombre}
                </p>
                <p className="text-sm text-gray-500">{e.ejercicio.grupo_muscular}</p>
              </li>
            ))}
          </ul>
        )}

        {/* Botones */}
        <div className="mt-10 text-center flex flex-wrap justify-center gap-4">
          {rutina.es_defecto ? (
            <button
              onClick={copiarRutina}
              className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded shadow"
            >
              <Copy size={18} /> Copiar rutina
            </button>
          ) : (
            <>
              <button
                onClick={iniciarSesion}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded shadow"
              >
                <Play size={18} /> Iniciar sesión de entrenamiento
              </button>

              <button
                onClick={editarRutina}
                className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-white px-5 py-2 rounded shadow"
              >
                <Pencil size={18} /> Editar rutina
              </button>

              <button
                onClick={eliminarRutina}
                className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded shadow"
              >
                <Trash size={18} /> Eliminar rutina
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
