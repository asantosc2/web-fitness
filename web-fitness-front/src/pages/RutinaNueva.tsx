// src/pages/RutinaNueva.tsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
}

interface EjercicioSeleccionado {
  ejercicio_id: number;
  orden: number;
  series: number;
  repeticiones: number;
  comentarios?: string;
}

export default function RutinaNueva() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [ejerciciosDisponibles, setEjerciciosDisponibles] = useState<Ejercicio[]>([]);
  const [seleccionados, setSeleccionados] = useState<EjercicioSeleccionado[]>([]);
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/ejercicios", {
      headers: { Authorization: `Bearer ${estado.token}` }
    })
      .then(res => res.json())
      .then(data => setEjerciciosDisponibles(data))
      .catch(err => console.error("Error cargando ejercicios", err));
  }, [estado.token]);

  const agregarEjercicio = () => {
    setSeleccionados([
      ...seleccionados,
      { ejercicio_id: 0, orden: seleccionados.length + 1, series: 3, repeticiones: 10 }
    ]);
  };

  const handleCambio = (index: number, campo: string, valor: any) => {
    const copia = [...seleccionados];
    (copia[index] as any)[campo] = valor;
    setSeleccionados(copia);
  };

  const guardarRutina = async () => {
    if (!nombre.trim()) return setMensaje("El nombre es obligatorio");
    try {
      const res = await fetch("http://localhost:8000/rutinas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`
        },
        body: JSON.stringify({ nombre, descripcion })
      });

      if (!res.ok) throw new Error("Error creando rutina");
      const rutina = await res.json();

      // Asociar ejercicios
      const res2 = await fetch(`http://localhost:8000/rutinas/${rutina.id}/ejercicios`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`
        },
        body: JSON.stringify(seleccionados)
      });

      if (!res2.ok) throw new Error("Error al añadir ejercicios");
      navigate(`/rutinas/${rutina.id}`);
    } catch (err: any) {
      console.error(err);
      setMensaje("No se pudo guardar la rutina");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">Nueva rutina</h1>

        {mensaje && <p className="text-red-500 mb-4 text-center">{mensaje}</p>}

        <div className="mb-4">
          <input
            type="text"
            placeholder="Nombre de la rutina"
            value={nombre}
            onChange={e => setNombre(e.target.value)}
            className="w-full border px-3 py-2 rounded"
          />
        </div>

        <div className="mb-6">
          <textarea
            placeholder="Descripción (opcional)"
            value={descripcion}
            onChange={e => setDescripcion(e.target.value)}
            className="w-full border px-3 py-2 rounded"
          />
        </div>

        <h2 className="font-semibold text-gray-700 mb-2">Ejercicios</h2>
        <div className="space-y-4 mb-6">
          {seleccionados.map((e, i) => (
            <div key={i} className="bg-white p-4 rounded shadow space-y-2">
              <select
                className="w-full border rounded px-2 py-1"
                value={e.ejercicio_id}
                onChange={ev => handleCambio(i, "ejercicio_id", Number(ev.target.value))}
              >
                <option value={0}>Selecciona ejercicio</option>
                {ejerciciosDisponibles.map(ej => (
                  <option key={ej.id} value={ej.id}>
                    {ej.nombre} ({ej.grupo_muscular})
                  </option>
                ))}
              </select>
              <div className="flex gap-2">
                <input
                  type="number"
                  placeholder="Series"
                  className="w-1/3 border rounded px-2 py-1"
                  value={e.series}
                  onChange={ev => handleCambio(i, "series", Number(ev.target.value))}
                />
                <input
                  type="number"
                  placeholder="Repeticiones"
                  className="w-1/3 border rounded px-2 py-1"
                  value={e.repeticiones}
                  onChange={ev => handleCambio(i, "repeticiones", Number(ev.target.value))}
                />
                <input
                  type="text"
                  placeholder="Comentarios"
                  className="w-full border rounded px-2 py-1"
                  value={e.comentarios || ""}
                  onChange={ev => handleCambio(i, "comentarios", ev.target.value)}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between">
          <button
            onClick={agregarEjercicio}
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
          >
            Añadir ejercicio
          </button>
          <button
            onClick={guardarRutina}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
          >
            Guardar rutina
          </button>
        </div>
      </div>
    </div>
  );
}
