import { useState } from "react";
import Navbar from "../components/Navbar";

interface Alimento {
  nombre: string;
  kcal: number;
  proteinas: number;
  carbohidratos: number;
  grasas: number;
  fibra?: number;
  imagen_url?: string;
}

export default function ConsultaNutricional() {
  const [busqueda, setBusqueda] = useState("");
  const [resultados, setResultados] = useState<Alimento[]>([]);
  const [cargando, setCargando] = useState(false);

  const buscar = async () => {
    if (!busqueda.trim()) return;
    setCargando(true);
    setResultados([]);
    try {
      const res = await fetch(`http://localhost:8000/alimentos/buscar-openfood?query=${busqueda}`);
      const data = await res.json();
      setResultados(data);
    } catch (err) {
      console.error("❌ Error al buscar alimentos:", err);
    }
    setCargando(false);
  };

  // 🔄 Manejar envío de formulario (tecla Enter)
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    buscar();
  };

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold mb-4 text-blue-600">Consulta Nutricional</h1>

        <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
          <input
            type="text"
            placeholder="Buscar alimento..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="flex-1 border px-4 py-2 rounded"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Buscar
          </button>
        </form>

        {cargando && <p className="text-gray-500 text-center">Buscando...</p>}

        {resultados.length > 0 && (
          <div className="space-y-3">
            {resultados.map((a, i) => (
              <div key={i} className="flex items-center gap-4 border rounded p-4 bg-gray-50">
                {a.imagen_url && (
                  <img
                    src={a.imagen_url}
                    alt={a.nombre}
                    className="w-20 h-20 object-cover rounded"
                  />
                )}
                <div>
                  <p className="font-semibold text-lg">{a.nombre}</p>
                  <p className="text-sm text-gray-600">
                    Calorías: {a.kcal} kcal | Proteínas: {a.proteinas} g | CH: {a.carbohidratos} g | Grasas: {a.grasas} g | Fibra: {a.fibra ?? 0} g
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
