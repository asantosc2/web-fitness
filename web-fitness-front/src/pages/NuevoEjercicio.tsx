import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const gruposMusculares = [
  "Brazos", "Hombros", "Espalda", "Pecho", "Piernas", "Glúteos", "Abdomen"
];

const categoriasEquipo = [
  "Mancuernas", "Barra", "Polea", "Máquina", "Peso corporal", "Banda elástica"
];

export default function NuevoEjercicio() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [nombre, setNombre] = useState("");
  const [grupo, setGrupo] = useState("");
  const [tipo, setTipo] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!nombre || !grupo || !tipo) {
      setError("Por favor completa los campos obligatorios");
      return;
    }

    const nuevo = {
      nombre,
      grupo_muscular: grupo,
      tipo_equipo: tipo,
      descripcion: descripcion.trim() || undefined,
    };

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/ejercicios`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify(nuevo),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Error al crear el ejercicio");
      }

      navigate("/ejercicios");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100 pt-24 px-4">
      <Navbar />
      <div className="max-w-xl mx-auto bg-white shadow-xl rounded-xl p-8">
        
        <button
          onClick={() => navigate(-1)}
          className="text-blue-600 hover:underline text-sm mb-4"
        >
          ⬅ Volver atrás
        </button>

        <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
          Crear nuevo ejercicio
        </h1>

        {error && (
          <p className="text-red-600 text-center font-semibold mb-4">{error}</p>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block font-medium text-gray-700 mb-1">Nombre *</label>
            <input
              type="text"
              value={nombre}
              onChange={e => setNombre(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Parte del cuerpo *</label>
            <select
              value={grupo}
              onChange={e => setGrupo(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="">-- Selecciona --</option>
              {gruposMusculares.map(g => (
                <option key={g} value={g}>{g}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Categoría *</label>
            <select
              value={tipo}
              onChange={e => setTipo(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="">-- Selecciona --</option>
              {categoriasEquipo.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Descripción (opcional)</label>
            <textarea
              value={descripcion}
              onChange={e => setDescripcion(e.target.value)}
              rows={4}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Guardar ejercicio
          </button>
        </form>
      </div>
    </div>
  );
}