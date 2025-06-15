import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

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
    fetch("http://localhost:8000/rutinas", {
      headers: { Authorization: `Bearer ${estado.token}` }
    })
      .then(res => res.json())
      .then(data => setRutinas(data))
      .catch(err => console.error("Error cargando rutinas:", err));
  }, [estado.token]);

  const misRutinas = rutinas.filter(r => !r.es_defecto && r.usuario_id === estado.usuario?.id);
  const ejemplos = rutinas.filter(r => r.es_defecto);

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">Mis plantillas</h1>

        <div className="flex justify-between items-center mb-6">
          <button
            onClick={() => setMostrarEjemplos(!mostrarEjemplos)}
            className="text-sm text-blue-600 underline"
          >
            {mostrarEjemplos ? "Ocultar ejemplos" : "Mostrar ejemplos"}
          </button>

          <button
            onClick={() => navigate("/rutinas/nueva")}
            className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
          >
            Crear nueva rutina
          </button>
        </div>

        <div className="space-y-3 mb-10">
          {misRutinas.map(r => (
            <div
              key={r.id}
              className="bg-white p-4 rounded shadow hover:bg-gray-50 cursor-pointer"
              onClick={() => navigate(`/rutinas/${r.id}`)}
            >
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-gray-800">{r.nombre}</h3>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded ml-2">Personal</span>
              </div>
              <p className="text-sm text-gray-500">{r.descripcion}</p>
            </div>
          ))}

        </div>

        {mostrarEjemplos && (
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-3">📂 Ejemplos de plantillas</h2>
            {ejemplos.length === 0 ? (
              <p className="text-gray-500 text-sm">No hay plantillas públicas.</p>
            ) : (
              <div className="space-y-3">
                {ejemplos.map(r => (
                  <div
                    key={r.id}
                    className="bg-white p-4 rounded shadow hover:bg-gray-50 cursor-pointer"
                    onClick={() => navigate(`/rutinas/${r.id}`)}
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-gray-800">{r.nombre}</h3>
                      <span className="text-xs bg-gray-300 text-gray-700 px-2 py-0.5 rounded ml-2">Ejemplo</span>
                    </div>
                    <p className="text-sm text-gray-500">{r.descripcion}</p>
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