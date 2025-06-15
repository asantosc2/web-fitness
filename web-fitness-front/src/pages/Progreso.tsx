import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

interface Foto {
  id: number;
  ruta: string;
}

interface Progreso {
  id: number;
  fecha: string;
  peso: number;
  comentarios?: string | null;
  fotos: Foto[];
}

export default function Progreso() {
  const { estado } = useAuth();
  const navigate = useNavigate();
  const [progresos, setProgresos] = useState<Progreso[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/progresos", {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then((res) => res.json())
      .then((data) => setProgresos(data))
      .catch((err) => console.error("Error cargando progresos", err));
  }, [estado.token]);

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-blue-600">Mi progreso</h1>
          <button
            onClick={() => navigate("/progreso/nuevo")}
            className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
          >
            Añadir registro
          </button>
        </div>

        {progresos.length === 0 ? (
          <p className="text-center text-gray-500">Sin registros aún</p>
        ) : (
          <div className="space-y-4">
            {progresos.map((p) => (
              <div
                key={p.id}
                onClick={() => navigate(`/progreso/${p.id}`)}
                className="bg-white p-4 rounded shadow cursor-pointer hover:shadow-md transition"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-800">
                      {new Date(p.fecha).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-500">{p.peso} kg</p>
                  </div>
                  {p.fotos[0] && (
                    <img
                      src={`http://localhost:8000/static/${p.fotos[0].ruta}`}
                      alt="Foto progreso"
                      className="h-16 w-16 object-cover rounded"
                    />
                  )}
                </div>
                {p.comentarios && (
                  <p className="mt-2 text-sm text-gray-600">{p.comentarios}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
