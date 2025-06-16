import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { ListPlus, BookOpen } from "lucide-react";

interface Rutina {
  id: number;
  nombre: string;
  descripcion?: string;
  es_defecto: boolean;
  usuario_id?: number;
}

export default function Rutinas() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [rutinas, setRutinas] = useState<Rutina[]>([]);
  const [mostrarEjemplos, setMostrarEjemplos] = useState(false);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/rutinas`, {
      headers: { Authorization: `Bearer ${estado.token}` }
    })
      .then(res => res.json())
      .then(data => setRutinas(data))
      .catch(err => console.error("Error cargando rutinas:", err));
  }, [estado.token]);

  const misRutinas = rutinas.filter(r => !r.es_defecto && r.usuario_id === estado.usuario?.id);
  const ejemplos = rutinas.filter(r => r.es_defecto);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-orange-700 mb-10">
          Mis Rutinas
        </h1>

        <div className="flex justify-between items-center mb-8">
          <button
            onClick={() => setMostrarEjemplos(!mostrarEjemplos)}
            className="text-sm font-medium text-orange-600 underline hover:text-orange-800"
          >
            {mostrarEjemplos ? "Ocultar ejemplos" : "Ver ejemplos de plantillas"}
          </button>

          <button
            onClick={() => navigate("/rutinas/nueva")}
            className="flex items-center gap-2 bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded shadow font-semibold transition"
          >
            <ListPlus size={20} /> Crear nueva rutina
          </button>
        </div>

        <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
          {misRutinas.map(r => (
            <div
              key={r.id}
              className="cursor-pointer bg-white p-5 rounded-xl shadow hover:shadow-lg transition"
              onClick={() => navigate(`/rutinas/${r.id}`)}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-gray-800">{r.nombre}</h3>
                <span className="text-xs bg-orange-100 text-orange-700 px-2 py-0.5 rounded font-medium">
                  Personal
                </span>
              </div>
              <p className="text-sm text-gray-600">{r.descripcion || "Sin descripción"}</p>
            </div>
          ))}
        </div>

        {mostrarEjemplos && (
          <div className="mt-12">
            <h2 className="text-xl font-bold text-orange-700 mb-4 flex items-center gap-2">
              <BookOpen size={20} /> Plantillas de ejemplo
            </h2>
            {ejemplos.length === 0 ? (
              <p className="text-sm text-gray-500">No hay rutinas de ejemplo disponibles.</p>
            ) : (
              <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
                {ejemplos.map(r => (
                  <div
                    key={r.id}
                    className="cursor-pointer bg-white p-5 rounded-xl shadow hover:shadow-lg transition"
                    onClick={() => navigate(`/rutinas/${r.id}`)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-xl font-semibold text-gray-800">{r.nombre}</h3>
                      <span className="text-xs bg-gray-300 text-gray-700 px-2 py-0.5 rounded font-medium">
                        Ejemplo
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{r.descripcion || "Sin descripción"}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}