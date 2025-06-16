import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { toast } from "react-hot-toast";

interface Sesion {
  id: number;
  fecha: string;
  rutina_id?: number | null;
  nombre_rutina?: string | null;
}

export default function HistorialSesiones() {
  const { estado } = useAuth();
  const navigate = useNavigate();
  const [sesiones, setSesiones] = useState<Sesion[]>([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/sesiones`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then((res) => res.json())
      .then((data) => setSesiones(data))
      .catch((err) => console.error("Error cargando sesiones:", err));
  }, [estado.token]);

  const eliminarSesion = async (id: number) => {
    const confirmar = confirm("¿Eliminar esta sesión?");
    if (!confirmar) return;
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/sesiones/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${estado.token}` },
      });

      if (!res.ok) throw new Error("No se pudo eliminar");
      setSesiones((prev) => prev.filter((s) => s.id !== id));
      toast.success("✅ Sesión eliminada");
    } catch (err) {
      toast.error("❌ Error al eliminar la sesión");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-700 mb-6 text-center">
          Historial de sesiones
        </h1>

        {sesiones.length === 0 ? (
          <p className="text-center text-gray-600">
            No hay sesiones registradas.
          </p>
        ) : (
          <ul className="space-y-3">
            {sesiones.map((s) => (
              <li
                key={s.id}
                className="bg-white p-4 rounded shadow flex justify-between items-center hover:bg-gray-50 transition"
              >
                <div
                  onClick={() => navigate(`/sesiones-historial/${s.id}`)}
                  className="cursor-pointer"
                >
                  <p className="font-semibold text-blue-700">
                    {new Date(s.fecha).toLocaleDateString()}
                  </p>
                  <p className="text-sm text-gray-500 truncate max-w-[220px]">
                    {s.nombre_rutina || "Rutina no especificada"}
                  </p>
                </div>
                <button
                  onClick={() => eliminarSesion(s.id)}
                  className="text-red-600 text-sm hover:underline"
                >
                  Eliminar
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}