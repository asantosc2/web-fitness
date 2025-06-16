// src/pages/RutinaNueva.tsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import {
  DragDropContext,
  Droppable,
  Draggable,
} from "@hello-pangea/dnd";
import type { DropResult } from "@hello-pangea/dnd";

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
  tipo_equipo: string;
  descripcion?: string;
}

interface Serie {
  numero: number;
  repeticiones: number | string;
  peso: number | string;
}

interface EjercicioSeleccionado {
  ejercicio: Ejercicio;
  orden: number;
  series: Serie[];
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
  const [filtroEjercicio, setFiltroEjercicio] = useState("");
  const [grupoFiltro, setGrupoFiltro] = useState("");
  const [equipoFiltro, setEquipoFiltro] = useState("");
  const [ejercicioSeleccionado, setEjercicioSeleccionado] = useState<Ejercicio | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/ejercicios`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then((res) => res.json())
      .then((data) => setEjerciciosDisponibles(data))
      .catch((err) => console.error("Error cargando ejercicios", err));
  }, [estado.token]);

  const agregarEjercicio = () => {
    if (!ejercicioSeleccionado) return;
    const nuevo: EjercicioSeleccionado = {
      ejercicio: ejercicioSeleccionado,
      orden: seleccionados.length + 1,
      series: [
        { numero: 1, repeticiones: 10, peso: 1 },
        { numero: 2, repeticiones: 10, peso: 1 },
        { numero: 3, repeticiones: 10, peso: 1 },
      ],
      comentarios: "",
    };
    setSeleccionados((prev) => [...prev, nuevo]);
    setEjercicioSeleccionado(null);
    setFiltroEjercicio("");
  };

  const actualizarSerie = (indexEj: number, indexSerie: number, campo: "peso" | "repeticiones", valor: string | number) => {
    const copia = [...seleccionados];
    copia[indexEj].series[indexSerie][campo] = valor;
    setSeleccionados(copia);
  };

  const añadirSerie = (indexEj: number) => {
    const copia = [...seleccionados];
    const nuevas = [...copia[indexEj].series, {
      numero: copia[indexEj].series.length + 1,
      repeticiones: 10,
      peso: 1,
    }];
    copia[indexEj].series = nuevas;
    setSeleccionados(copia);
  };

  const eliminarSerie = (indexEj: number, indexSerie: number) => {
    const confirmar = confirm("¿Eliminar esta serie?");
    if (!confirmar) return;
    const copia = [...seleccionados];
    copia[indexEj].series.splice(indexSerie, 1);
    copia[indexEj].series.forEach((s, i) => (s.numero = i + 1));
    setSeleccionados(copia);
  };

  const eliminarEjercicio = (index: number) => {
    const confirmar = confirm("¿Eliminar este ejercicio y sus series?");
    if (!confirmar) return;
    const copia = [...seleccionados];
    copia.splice(index, 1);
    copia.forEach((e, i) => (e.orden = i + 1));
    setSeleccionados(copia);
  };

  const guardarRutina = async () => {
    if (!nombre.trim()) return setMensaje("El nombre es obligatorio");
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/rutinas`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify({ nombre, descripcion }),
      });

      if (!res.ok) throw new Error("Error creando rutina");
      const rutina = await res.json();

      for (const [i, ej] of seleccionados.entries()) {
        const resEj = await fetch(`${import.meta.env.VITE_API_URL}/rutinas/${rutina.id}/ejercicios`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${estado.token}`,
          },
          body: JSON.stringify({
            ejercicio_id: ej.ejercicio.id,
            orden: i + 1,
            series: ej.series.length,
            repeticiones: ej.series[0]?.repeticiones || 10,
            comentarios: ej.comentarios || "",
          })
        });

        if (resEj.ok) {
          const rel = await resEj.json();
          await fetch(`${import.meta.env.VITE_API_URL}/rutina-ejercicio/${rel.id}/series`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${estado.token}`,
            },
            body: JSON.stringify(ej.series),
          });
        }
      }

      navigate(`/rutinas/${rutina.id}`);
    } catch (err: any) {
      console.error(err);
      setMensaje("No se pudo guardar la rutina");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 to-indigo-100 pt-24 px-4">
      <Navbar />
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-blue-700 mb-10">Nueva Rutina</h1>

        {mensaje && <p className="text-red-600 text-center mb-4 font-medium">{mensaje}</p>}

        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8 space-y-4">
          <input
            type="text"
            placeholder="Nombre de la rutina"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            className="w-full border px-4 py-2 rounded-md shadow-sm"
          />
          <textarea
            placeholder="Descripción (opcional)"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            className="w-full border px-4 py-2 rounded-md shadow-sm"
          />
        </div>

        <DragDropContext onDragEnd={({ source, destination }: DropResult) => {
          if (!destination || destination.index === source.index) return;
          const copia = [...seleccionados];
          const [movido] = copia.splice(source.index, 1);
          copia.splice(destination.index, 0, movido);
          copia.forEach((e, i) => (e.orden = i + 1));
          setSeleccionados(copia);
        }}>
          <Droppable droppableId="ejercicios">
            {(provided) => (
              <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-4">
                {seleccionados.map((ej, i) => (
                  <Draggable key={i} draggableId={i.toString()} index={i}>
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className="bg-white rounded-xl shadow p-4"
                      >
                        <div className="flex justify-between items-center">
                          <h2 className="font-semibold text-blue-700 text-lg">{ej.ejercicio.nombre}</h2>
                          <button
                            onClick={() => eliminarEjercicio(i)}
                            className="text-red-600 text-sm hover:underline"
                          >
                            Eliminar
                          </button>
                        </div>
                        <p className="text-sm text-gray-600">Grupo: {ej.ejercicio.grupo_muscular}</p>

                        <div className="grid grid-cols-3 gap-2 mt-2 text-sm font-semibold text-gray-500">
                          <span>Serie</span>
                          <span>Peso</span>
                          <span>Reps</span>
                        </div>

                        {ej.series.map((s, idx) => (
                          <div key={idx} className="grid grid-cols-4 gap-2 items-center my-1">
                            <span className="text-sm">{s.numero}</span>
                            <input
                              type="number"
                              value={s.peso}
                              onChange={(e) => actualizarSerie(i, idx, "peso", e.target.value)}
                              className="border rounded px-2 py-1"
                            />
                            <input
                              type="number"
                              value={s.repeticiones}
                              onChange={(e) => actualizarSerie(i, idx, "repeticiones", e.target.value)}
                              className="border rounded px-2 py-1"
                            />
                            <button
                              onClick={() => eliminarSerie(i, idx)}
                              className="text-red-500 hover:underline text-xs"
                            >
                              🗑
                            </button>
                          </div>
                        ))}

                        <button
                          onClick={() => añadirSerie(i)}
                          className="text-blue-600 text-sm mt-2 hover:underline"
                        >
                          ➕ Añadir serie
                        </button>
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        {/* SELECCIÓN DE EJERCICIO */}
        <div className="bg-white rounded-2xl shadow-md mt-10 p-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Añadir ejercicio</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
            <input
              type="text"
              placeholder="Buscar por nombre"
              value={filtroEjercicio}
              onChange={(e) => setFiltroEjercicio(e.target.value)}
              className="border px-3 py-2 rounded"
            />
            <select
              value={grupoFiltro}
              onChange={(e) => setGrupoFiltro(e.target.value)}
              className="border px-3 py-2 rounded"
            >
              <option value="">Todos los grupos</option>
              {[...new Set(ejerciciosDisponibles.map(e => e.grupo_muscular))].map(grupo => (
                <option key={grupo} value={grupo}>{grupo}</option>
              ))}
            </select>
            <select
              value={equipoFiltro}
              onChange={(e) => setEquipoFiltro(e.target.value)}
              className="border px-3 py-2 rounded"
            >
              <option value="">Todos los equipos</option>
              {[...new Set(ejerciciosDisponibles.map(e => e.tipo_equipo))].map(equipo => (
                <option key={equipo} value={equipo}>{equipo}</option>
              ))}
            </select>
          </div>

          <div className="max-h-40 overflow-y-auto border rounded">
            {ejerciciosDisponibles
              .filter(e =>
                e.nombre.toLowerCase().includes(filtroEjercicio.toLowerCase()) &&
                (!grupoFiltro || e.grupo_muscular === grupoFiltro) &&
                (!equipoFiltro || e.tipo_equipo === equipoFiltro)
              )
              .sort((a, b) => a.nombre.localeCompare(b.nombre))
              .slice(0, 10)
              .map(e => (
                <div
                  key={e.id}
                  onClick={() => setEjercicioSeleccionado(e)}
                  className="px-3 py-2 cursor-pointer hover:bg-gray-200"
                >
                  {e.nombre} ({e.grupo_muscular} - {e.tipo_equipo})
                </div>
              ))}
          </div>

          {ejercicioSeleccionado && (
            <div className="mt-2 text-sm text-green-600">
              ✅ {ejercicioSeleccionado.nombre} listo para añadir
            </div>
          )}

          <button
            onClick={agregarEjercicio}
            className="mt-4 bg-green-600 text-white w-full py-2 rounded hover:bg-green-700"
          >
            Añadir ejercicio
          </button>
        </div>

        <button
          onClick={guardarRutina}
          className="mt-8 bg-blue-600 hover:bg-blue-700 text-white w-full py-3 rounded-lg font-semibold text-lg"
        >
          Guardar rutina
        </button>
      </div>
    </div>
  );
}