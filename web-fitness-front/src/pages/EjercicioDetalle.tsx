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
  imagen_url?: string | null;
}

export default function EjercicioDetalle() {
  const { id } = useParams<{ id: string }>();
  const { estado } = useAuth();
  const navigate = useNavigate();
  const [ejercicio, setEjercicio] = useState<Ejercicio | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/ejercicios/${id}`, {
      headers: {
        Authorization: `Bearer ${estado.token}`,
      },
    })
      .then(res => res.json())
      .then(data => setEjercicio(data))
      .catch(err => {
        console.error("Error al cargar ejercicio", err);
        navigate("/ejercicios");
      });
  }, [id, estado.token, navigate]);

  if (!ejercicio) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100 pt-24 px-4">
      <Navbar />
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-xl p-6 relative">
        <button
          onClick={() => navigate(-1)}
          className="absolute top-4 left-4 text-sm text-blue-600 hover:underline"
        >
          ⬅ Volver
        </button>

        <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
          {ejercicio.nombre}
        </h1>

        {ejercicio.imagen_url ? (
          <img
            src={ejercicio.imagen_url}
            alt={ejercicio.nombre}
            className="w-full h-64 object-cover rounded-lg shadow mb-6"
          />
        ) : (
          <div className="w-full h-64 bg-gray-200 rounded-lg mb-6 flex items-center justify-center text-gray-500 text-lg">
            Sin imagen disponible
          </div>
        )}

        <div className="space-y-3 text-gray-700 text-lg">
          <p>
            <span className="font-semibold text-gray-800">Grupo muscular:</span>{" "}
            {ejercicio.grupo_muscular}
          </p>
          <p>
            <span className="font-semibold text-gray-800">Tipo de equipo:</span>{" "}
            {ejercicio.tipo_equipo}
          </p>
          {ejercicio.descripcion && (
            <p className="pt-4 whitespace-pre-wrap">
              <span className="block font-semibold text-gray-800 mb-1">Descripción:</span>
              {ejercicio.descripcion}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}