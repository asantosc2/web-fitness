import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function ProgresoNuevo() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [peso, setPeso] = useState(0);
  const [comentarios, setComentarios] = useState("");
  const [fotos, setFotos] = useState<FileList | null>(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://localhost:8000/progresos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify({
          fecha: new Date().toISOString().split("T")[0],
          peso,
          comentarios: comentarios.trim() || null,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al guardar");
      }

      const progreso = await res.json();

      if (fotos && fotos.length > 0) {
        const formData = new FormData();
        Array.from(fotos).forEach((f) => formData.append("archivos", f));
        await fetch(`http://localhost:8000/progresos/${progreso.id}/fotos`, {
          method: "POST",
          headers: { Authorization: `Bearer ${estado.token}` },
          body: formData,
        });
      }

      navigate("/progreso");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-lg mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold mb-4 text-blue-600">Nuevo progreso</h1>
        {error && <p className="text-red-600 mb-2 text-sm">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-semibold mb-1">Peso (kg)</label>
            <input
              type="number"
              step="0.1"
              value={peso}
              onChange={(e) => setPeso(parseFloat(e.target.value))}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Comentarios</label>
            <textarea
              value={comentarios}
              onChange={(e) => setComentarios(e.target.value)}
              rows={3}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Fotos</label>
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={(e) => setFotos(e.target.files)}
            />
            <p className="text-xs text-gray-500 mt-1">Máximo 10 imágenes</p>
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Guardar
          </button>
        </form>
      </div>
    </div>
  );
}
