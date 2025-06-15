import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

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
      const res = await fetch("http://localhost:8000/ejercicios", {
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
    <div className="min-h-screen bg-gray-100 pt-24 px-6 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold text-blue-600 mb-8 text-center">
        Crear nuevo ejercicio
      </h1>

      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-6 space-y-4">
        {error && <p className="text-red-600 font-semibold text-sm">{error}</p>}

        <div>
          <label className="block font-semibold mb-1">Nombre *</label>
          <input
            type="text"
            value={nombre}
            onChange={e => setNombre(e.target.value)}
            className="w-full border rounded px-3 py-2"
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">Parte del cuerpo *</label>
          <select
            value={grupo}
            onChange={e => setGrupo(e.target.value)}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">-- Selecciona --</option>
            {gruposMusculares.map(g => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block font-semibold mb-1">Categoría *</label>
          <select
            value={tipo}
            onChange={e => setTipo(e.target.value)}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">-- Selecciona --</option>
            {categoriasEquipo.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block font-semibold mb-1">Descripción (opcional)</label>
          <textarea
            value={descripcion}
            onChange={e => setDescripcion(e.target.value)}
            rows={4}
            className="w-full border rounded px-3 py-2"
          />
        </div>

        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Guardar ejercicio
        </button>
      </form>
    </div>
  );
}
