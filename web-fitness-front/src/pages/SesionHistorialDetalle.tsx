import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { toast } from "react-hot-toast";

interface Serie {
  id: number;
  numero: number;
  repeticiones: number;
  peso: number;
}

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
  tipo_equipo?: string;
}

interface SesionEjercicio {
  id: number;
  orden: number;
  repeticiones: number;
  series: number;
  peso: number;
  comentarios?: string;
  ejercicio: Ejercicio;
  series_detalle: Serie[];
}

export default function SesionHistorialDetalle() {
  const { id } = useParams();
  const { estado } = useAuth();
  const navigate = useNavigate();
  const [ejercicios, setEjercicios] = useState<SesionEjercicio[]>([]);

  useEffect(() => {
    if (!id) return;
    fetch(`${import.meta.env.VITE_API_URL}/sesiones/${id}/ejercicios`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then((res) => res.json())
      .then(async (data) => {
        const completos = await Promise.all(
          data.map(async (ej: SesionEjercicio) => {
            const resSeries = await fetch(
              `${import.meta.env.VITE_API_URL}/sesion-ejercicio/${ej.id}/series`,
              { headers: { Authorization: `Bearer ${estado.token}` } }
            );
            const series = await resSeries.json();
            return { ...ej, series_detalle: series };
          })
        );
        setEjercicios(completos);
      })
      .catch((err) => console.error("Error al cargar sesión", err));
  }, [id, estado.token]);

  const eliminarSesion = async () => {
    if (!id) return;
    const confirmar = confirm("¿Eliminar esta sesión?");
    if (!confirmar) return;

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/sesiones/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${estado.token}` },
      });

      if (!res.ok) throw new Error("Error al eliminar sesión");

      toast.success("✅ Sesión eliminada");
      navigate("/sesiones-historial");
    } catch (err) {
      console.error(err);
      toast.error("❌ Error al eliminar sesión");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto">
        <button
          onClick={() => navigate(-1)}
          className="text-blue-700 hover:underline mb-4"
        >
          ⬅ Volver atrás
        </button>
        <h1 className="text-3xl font-bold text-blue-700 mb-6 text-center">
          Detalle de la sesión
        </h1>
        {ejercicios.length === 0 ? (
          <p className="text-center text-gray-600">Cargando ejercicios...</p>
        ) : (
          <ul className="space-y-4">
            {ejercicios.map((ej) => (
              <li key={ej.id} className="bg-white p-4 rounded shadow">
                <h2 className="font-semibold text-blue-700 text-lg">
                  {ej.ejercicio.nombre}
                </h2>
                <p className="text-sm text-gray-500 mb-2">
                  Grupo: {ej.ejercicio.grupo_muscular}
                </p>
                <div className="grid grid-cols-3 font-semibold text-sm mt-2 text-gray-600">
                  <span>Serie</span>
                  <span>Peso</span>
                  <span>Reps</span>
                </div>
                {ej.series_detalle.map((s) => (
                  <div
                    key={s.id}
                    className="grid grid-cols-3 gap-2 my-1 items-center"
                  >
                    <span className="text-sm">{s.numero}</span>
                    <span className="text-sm">{s.peso}</span>
                    <span className="text-sm">{s.repeticiones}</span>
                  </div>
                ))}
              </li>
            ))}
          </ul>
        )}
        <div className="text-center mt-6">
          <button
            onClick={eliminarSesion}
            className="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700"
          >
            Eliminar sesión
          </button>
        </div>
      </div>
    </div>
  );
}