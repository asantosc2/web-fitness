// EditarRutina.tsx
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
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
  id?: number;
  numero: number;
  repeticiones: number | string;
  peso: number | string;
}

interface RutinaEjercicio {
  id: number;
  ejercicio_id: number;
  orden: number;
  series: number;
  repeticiones: number;
  comentarios?: string;
  ejercicio: Ejercicio;
}

export default function EditarRutina() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { estado } = useAuth();

  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [ejercicios, setEjercicios] = useState<RutinaEjercicio[]>([]);
  const [series, setSeries] = useState<{ [key: number]: Serie[] }>({});
  const [todosEjercicios, setTodosEjercicios] = useState<Ejercicio[]>([]);
  const [filtroEjercicio, setFiltroEjercicio] = useState("");
  const [ejercicioSeleccionado, setEjercicioSeleccionado] = useState<Ejercicio | null>(null);
  const [grupoFiltro, setGrupoFiltro] = useState("");
  const [equipoFiltro, setEquipoFiltro] = useState("");


  useEffect(() => {
    fetch(`http://localhost:8000/rutinas/${id}`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then(res => res.json())
      .then(data => {
        setNombre(data.nombre);
        setDescripcion(data.descripcion || "");
      });

    fetch(`http://localhost:8000/rutinas/${id}/ejercicios`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then(res => res.json())
      .then(data => {
        setEjercicios(data);
        data.forEach((ej: RutinaEjercicio) => {
          cargarSeries(ej.id, ej.series, ej.repeticiones);
        });
      });

    fetch("http://localhost:8000/ejercicios", {
      headers: { Authorization: `Bearer ${estado.token}` },
    })
      .then(res => res.json())
      .then(setTodosEjercicios);
  }, [id, estado.token]);

  const cargarSeries = async (rutinaEjercicioId: number, cantidad: number, repeticiones: number) => {
    const res = await fetch(`http://localhost:8000/rutina-ejercicio/${rutinaEjercicioId}/series`, {
      headers: { Authorization: `Bearer ${estado.token}` },
    });

    if (!res.ok) return;

    const data = await res.json();
    data.sort((a: Serie, b: Serie) => a.numero - b.numero);

    if (data.length > 0) {
      setSeries(prev => ({ ...prev, [rutinaEjercicioId]: data }));
    } else {
      const nuevasSeries = Array.from({ length: cantidad || 3 }).map((_, i) => ({
        numero: i + 1,
        repeticiones: repeticiones || 10,
        peso: 1,
      }));

      const crear = await fetch(`http://localhost:8000/rutina-ejercicio/${rutinaEjercicioId}/series`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify(nuevasSeries),
      });

      if (crear.ok) {
        const creadas = await crear.json();
        setSeries(prev => ({ ...prev, [rutinaEjercicioId]: creadas }));
      }
    }
  };

  const actualizarCampoSerie = async (rutinaEjId: number, index: number, campo: "peso" | "repeticiones", valor: number) => {
    const lista = [...(series[rutinaEjId] || [])];
    lista[index][campo] = valor;
    setSeries(prev => ({ ...prev, [rutinaEjId]: lista }));

    const s = lista[index];

    if (s.id) {
      const res = await fetch(`http://localhost:8000/rutina-serie/${s.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify({ [campo]: valor }),
      });

      if (!res.ok) {
        console.error(`❌ Error al actualizar la serie con ID ${s.id}`);
        const error = await res.json();
        console.error(error);
      }
    }
  };

  const eliminarSerie = async (rutinaEjId: number, serieId?: number, index?: number) => {
    if (!serieId || index === undefined) return;
    const confirmar = confirm("¿Seguro que quieres eliminar esta serie?");
    if (!confirmar) return;

    const res = await fetch(`http://localhost:8000/rutina-serie/${serieId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${estado.token}` },
    });

    if (res.ok) {
      const nuevas = [...(series[rutinaEjId] || [])];
      nuevas.splice(index, 1);
      nuevas.forEach((s, i) => (s.numero = i + 1));
      setSeries(prev => ({ ...prev, [rutinaEjId]: nuevas }));
    } else {
      console.error("❌ No se pudo eliminar la serie");
    }
  };

  const añadirSerie = async (rutinaEjId: number) => {
    const actuales = series[rutinaEjId] || [];
    const nuevaSerie = {
      numero: actuales.length + 1,
      peso: 1,
      repeticiones: 10,
    };

    const res = await fetch(`http://localhost:8000/rutina-ejercicio/${rutinaEjId}/series`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${estado.token}`,
      },
      body: JSON.stringify([nuevaSerie]),
    });

    if (res.ok) {
      const [creada] = await res.json();
      setSeries(prev => ({ ...prev, [rutinaEjId]: [...actuales, creada] }));
    }
  };

  const eliminarEjercicio = async (rutinaEjId: number) => {
    const confirmar = confirm("¿Seguro que quieres eliminar este ejercicio y todas sus series?");
    if (!confirmar) return;

    const res = await fetch(`http://localhost:8000/rutina-ejercicio/${rutinaEjId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${estado.token}` },
    });

    if (res.ok) {
      setEjercicios(prev => prev.filter(e => e.id !== rutinaEjId));
      setSeries(prev => {
        const copia = { ...prev };
        delete copia[rutinaEjId];
        return copia;
      });
    } else {
      alert("❌ No se pudo eliminar el ejercicio.");
    }
  };

  const actualizarOrden = async (nuevos: RutinaEjercicio[]) => {
    const actualizados = nuevos.map((ej, i) => ({ id: ej.id, orden: i + 1 }));

    const res = await fetch("http://localhost:8000/rutina-ejercicio/orden", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${estado.token}`,
      },
      body: JSON.stringify(actualizados),
    });

    if (res.ok) {
      setEjercicios(nuevos.map((e, i) => ({ ...e, orden: i + 1 })));
    } else {
      const error = await res.json();
      console.error("❌ Detalle del error:", JSON.stringify(error, null, 2));
      alert("❌ Error al actualizar el orden");
    }
  };

  const guardarCambios = async () => {
    try {
      const res = await fetch(`http://localhost:8000/rutinas/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${estado.token}`,
        },
        body: JSON.stringify({ nombre, descripcion }),
      });

      if (!res.ok) {
        const error = await res.json();
        alert(error.detail || "Error al guardar la rutina");
        return;
      }

      alert("✅ Cambios guardados.");
    } catch (err) {
      console.error("Error al guardar:", err);
      alert("Error inesperado");
    }
  };

  const agregarEjercicio = async () => {
    if (!ejercicioSeleccionado) return;

    const orden = ejercicios.length + 1;
    const res = await fetch(`http://localhost:8000/rutinas/${id}/ejercicios`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${estado.token}`,
      },
      body: JSON.stringify({ ejercicio_id: ejercicioSeleccionado.id, orden }),
    });

    if (!res.ok) {
      alert("❌ Error al agregar ejercicio");
      return;
    }

    const nuevo = await res.json();
    setEjercicios(prev => [...prev, nuevo]);
    await cargarSeries(nuevo.id, 3, 10);
    setEjercicioSeleccionado(null);
  };

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between mb-4">
          <button onClick={() => navigate(-1)} className="text-blue-600 hover:underline">⬅ Atrás</button>
          <button onClick={guardarCambios} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">💾 Guardar cambios</button>
        </div>

        <h1 className="text-3xl font-bold text-blue-600 text-center mb-6">Editar rutina</h1>

        <input value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Nombre de la rutina" className="w-full border p-2 rounded mb-2" />
        <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} placeholder="Descripción" className="w-full border p-2 rounded mb-4" />

        <DragDropContext onDragEnd={({ source, destination }: DropResult) => {
          if (!destination || destination.index === source.index) return;
          const copia = [...ejercicios];
          const [movido] = copia.splice(source.index, 1);
          copia.splice(destination.index, 0, movido);
          setEjercicios(copia);
          actualizarOrden(copia);
        }}>
          <Droppable droppableId="ejercicios-droppable">
            {(provided) => (
              <div ref={provided.innerRef} {...provided.droppableProps}>
                {ejercicios.map((ej, index) => (
                  <Draggable key={ej.id} draggableId={ej.id.toString()} index={index}>
                    {(provided) => (
                      <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} className="bg-white p-4 rounded shadow mb-4">
                        <div className="flex justify-between items-center mb-1">
                          <h2 className="font-semibold text-blue-700 text-lg">{ej.ejercicio.nombre}</h2>
                          <button onClick={() => eliminarEjercicio(ej.id)} className="text-red-500 text-xs hover:underline">Eliminar ejercicio</button>
                        </div>
                        <p className="text-sm text-gray-500 mb-2">Grupo: {ej.ejercicio.grupo_muscular}</p>

                        <div className="grid grid-cols-3 font-semibold text-sm mt-2 text-gray-600">
                          <span>Serie</span>
                          <span>Peso</span>
                          <span>Reps</span>
                        </div>

                        {series[ej.id]?.map((s, idx) => (
                          <div key={idx} className="grid grid-cols-4 gap-2 my-1 items-center">
                            <span className="text-sm">{s.numero}</span>
                            <input type="number" min={0} value={s.peso} onChange={(e) => {
                              const lista = [...(series[ej.id] || [])];
                              lista[idx].peso = e.target.value;
                              setSeries(prev => ({ ...prev, [ej.id]: lista }));
                            }} onBlur={(e) => {
                              const val = parseFloat(e.target.value);
                              if (!isNaN(val)) actualizarCampoSerie(ej.id, idx, "peso", val);
                            }} className="border rounded p-1" />
                            <input type="number" min={0} value={s.repeticiones} onChange={(e) => {
                              const lista = [...(series[ej.id] || [])];
                              lista[idx].repeticiones = e.target.value;
                              setSeries(prev => ({ ...prev, [ej.id]: lista }));
                            }} onBlur={(e) => {
                              const val = parseInt(e.target.value);
                              if (!isNaN(val)) actualizarCampoSerie(ej.id, idx, "repeticiones", val);
                            }} className="border rounded p-1" />
                            <button onClick={() => eliminarSerie(ej.id, s.id, idx)} className="text-red-500 text-xs hover:underline">🗑</button>
                          </div>
                        ))}

                        <button onClick={() => añadirSerie(ej.id)} className="text-blue-600 text-sm mt-2 hover:underline">➕ Añadir serie</button>
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        <div className="bg-white p-4 rounded shadow mt-8">
          <h2 className="text-lg font-semibold text-gray-700 mb-4">➕ Añadir nuevo ejercicio</h2>

          <div className="grid gap-2 grid-cols-1 sm:grid-cols-3 mb-3">
            <input
              type="text"
              placeholder="Buscar por nombre"
              value={filtroEjercicio}
              onChange={(e) => setFiltroEjercicio(e.target.value)}
              className="border px-3 py-2 rounded shadow-sm"
            />
            <select
              value={grupoFiltro}
              onChange={(e) => setGrupoFiltro(e.target.value)}
              className="border px-3 py-2 rounded shadow-sm"
            >
              <option value="">Todas las partes del cuerpo</option>
              {[...new Set(todosEjercicios.map(e => e.grupo_muscular))].map(grupo => (
                <option key={grupo} value={grupo}>{grupo}</option>
              ))}
            </select>
            <select
              value={equipoFiltro}
              onChange={(e) => setEquipoFiltro(e.target.value)}
              className="border px-3 py-2 rounded shadow-sm"
            >
              <option value="">Todos los equipos</option>
              {[...new Set(todosEjercicios.map(e => e.tipo_equipo))].map(equipo => (
                <option key={equipo} value={equipo}>{equipo}</option>
              ))}
            </select>
          </div>

          <div className="max-h-40 overflow-y-auto border rounded">
            {todosEjercicios
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
                  onClick={() => {
                    setEjercicioSeleccionado(e);
                    setFiltroEjercicio("");
                  }}
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
            className="mt-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full"
          >
            Añadir ejercicio
          </button>
        </div>

      </div>
    </div>
  );
}
