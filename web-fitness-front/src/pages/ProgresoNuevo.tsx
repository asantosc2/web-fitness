import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { toast } from "react-hot-toast";

export default function ProgresoNuevo() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [peso, setPeso] = useState(0);
  const [comentarios, setComentarios] = useState("");
  const [fotos, setFotos] = useState<FileList | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/progresos`, {
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
        await fetch(`${import.meta.env.VITE_API_URL}/progresos/${progreso.id}/fotos`, {
          method: "POST",
          headers: { Authorization: `Bearer ${estado.token}` },
          body: formData,
        });
      }

      toast.success("✅ Progreso guardado");
      navigate("/progreso");
    } catch (err: any) {
      toast.error(err.message || "❌ Error inesperado");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-violet-200 pt-24 px-6">
      <Navbar />
      <div className="max-w-lg mx-auto bg-white p-6 rounded-xl shadow">
        <button
          onClick={() => navigate(-1)}
          className="text-purple-600 hover:underline text-sm mb-4"
        >
          ⬅ Volver atrás
        </button>

        <h1 className="text-2xl font-bold mb-4 text-purple-700">Nuevo progreso</h1>

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
            className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 w-full"
          >
            Guardar
          </button>
        </form>
      </div>
    </div>
  );
}
