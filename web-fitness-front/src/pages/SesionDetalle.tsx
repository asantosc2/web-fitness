// src/pages/SesionDetalle.tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import { DragDropContext, Draggable, Droppable, type DropResult } from "@hello-pangea/dnd";


interface Serie {
    id: number;
    numero: number;
    repeticiones: number;
    peso: number;
    completada?: boolean;
}

interface Ejercicio {
    id: number;
    nombre: string;
    grupo_muscular: string;
    tipo_equipo?: string;
}
interface Sesion {
    id: number;
    fecha: string;
    nombre_rutina?: string | null;
}

interface SesionEjercicio {
    id: number;
    orden: number;
    repeticiones: number;
    series: number;
    peso: number;
    comentarios?: string;
    ejercicio: Ejercicio;
    series_detalle: Serie[];
}

export default function SesionDetalle() {
    const { id } = useParams();
    const { estado } = useAuth();
    const navigate = useNavigate();
    const [ejercicios, setEjercicios] = useState<SesionEjercicio[]>([]);
    const [ejerciciosDisponibles, setEjerciciosDisponibles] = useState<Ejercicio[]>([]);
    const [filtro, setFiltro] = useState("");
    const [ejercicioSeleccionado, setEjercicioSeleccionado] = useState<Ejercicio | null>(null);
    const [grupoSeleccionado, setGrupoSeleccionado] = useState("");
    const [tipoSeleccionado, setTipoSeleccionado] = useState("");
    const [sesion, setSesion] = useState<Sesion | null>(null);

    useEffect(() => {
        if (!id) return;
        fetch(`http://localhost:8000/sesiones`, {
            headers: { Authorization: `Bearer ${estado.token}` },
        })
            .then(res => res.json())
            .then(data => {
                const encontrada = data.find((s: Sesion) => s.id === Number(id));
                setSesion(encontrada || null);
            });
    }, [id, estado.token]);


    useEffect(() => {
        fetch("http://localhost:8000/ejercicios", {
            headers: { Authorization: `Bearer ${estado.token}` },
        })
            .then(res => res.json())
            .then(data => setEjerciciosDisponibles(data))
            .catch(err => console.error("Error al cargar ejercicios disponibles", err));
    }, [estado.token]);

    useEffect(() => {
        if (!id) return;
        fetch(`http://localhost:8000/sesiones/${id}/ejercicios`, {
            headers: { Authorization: `Bearer ${estado.token}` },
        })
            .then(res => res.json())
            .then(async data => {
                const ejerciciosConSeries = await Promise.all(
                    data.map(async (ej: SesionEjercicio) => {
                        const res = await fetch(`http://localhost:8000/sesion-ejercicio/${ej.id}/series`, {
                            headers: { Authorization: `Bearer ${estado.token}` },
                        });
                        const series = await res.json();
                        return { ...ej, series_detalle: series };
                    })
                );
                setEjercicios(ejerciciosConSeries);
            })
            .catch(err => console.error("Error al cargar sesión", err));
    }, [id, estado.token]);


    const añadirSerie = async (sesionEjercicioId: number, index: number) => {
        const nueva = {
            numero: ejercicios[index].series_detalle.length + 1,
            repeticiones: 10,
            peso: 1,
        };

        const res = await fetch(`http://localhost:8000/sesion-ejercicio/${sesionEjercicioId}/series`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${estado.token}`,
            },
            body: JSON.stringify([nueva]),
        });

        const nuevas = await res.json();
        const copia = [...ejercicios];
        copia[index].series_detalle.push(...nuevas);
        setEjercicios(copia);
    };
    const eliminarEjercicio = async (ejercicioId: number) => {
        const confirmar = confirm("¿Seguro que quieres eliminar este ejercicio?");
        if (!confirmar) return;

        await fetch(`http://localhost:8000/sesion-ejercicio/${ejercicioId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${estado.token}`,
            },
        });

        setEjercicios((prev) => prev.filter((ej) => ej.id !== ejercicioId));
    };


    const eliminarSerie = async (serieId: number, ejercicioIndex: number, serieIndex: number) => {
        const confirmar = confirm("¿Eliminar esta serie?");
        if (!confirmar) return;

        await fetch(`http://localhost:8000/sesion-serie/${serieId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${estado.token}` },
        });

        const copia = [...ejercicios];
        copia[ejercicioIndex].series_detalle.splice(serieIndex, 1);
        copia[ejercicioIndex].series_detalle.forEach((s, i) => (s.numero = i + 1));
        setEjercicios(copia);
    };

    const agregarEjercicio = async () => {
        if (!id || !ejercicioSeleccionado) return;

        const nuevoEjercicio = {
            ejercicio_id: ejercicioSeleccionado.id,
            orden: ejercicios.length + 1,
            series: 3,
            repeticiones: 10,
            peso: 1,
            comentarios: "",
        };

        const res = await fetch(`http://localhost:8000/sesiones/${id}/ejercicios`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${estado.token}`,
            },
            body: JSON.stringify([nuevoEjercicio]),
        });

        const data = await res.json();
        const resSeries = await fetch(`http://localhost:8000/sesion-ejercicio/${data[0].id}/series`, {
            headers: { Authorization: `Bearer ${estado.token}` },
        });
        const series = await resSeries.json();

        setEjercicios((prev) => [...prev, { ...data[0], series_detalle: series }]);
        setEjercicioSeleccionado(null);
        setFiltro("");
    };
    const guardarSeriesSesion = async () => {
        for (const ej of ejercicios) {
            for (const s of ej.series_detalle) {
                await fetch(`http://localhost:8000/sesion-serie/${s.id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${estado.token}`,
                    },
                    body: JSON.stringify({
                        peso: Number(s.peso),
                        repeticiones: Number(s.repeticiones),
                    }),
                });
            }
        }
    };

    const finalizarSesion = async () => {
        const confirmar = confirm("¿Deseas finalizar esta sesión y actualizar la rutina base?");
        if (!confirmar || !id) return;

        try {
            await guardarSeriesSesion(); // ✅ Guardar cambios antes de enviar
            // 🔄 Guardar orden de los ejercicios
            await fetch(`http://localhost:8000/sesiones/${id}/orden-ejercicios`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${estado.token}`,
                },
                body: JSON.stringify(
                    ejercicios.map((ej) => ({
                        sesion_ejercicio_id: ej.id,
                        nuevo_orden: ej.orden,
                    }))
                ),
            });
            const res = await fetch(`http://localhost:8000/sesiones/${id}/actualizar-rutina`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${estado.token}`,
                },
            });

            if (!res.ok) throw new Error("Error al actualizar la rutina");

            alert("✅ Rutina actualizada correctamente.");
            navigate("/rutinas");
        } catch (err) {
            console.error(err);
            alert("❌ Error al actualizar la rutina desde la sesión.");
        }
    };


    const cancelarSesion = async () => {
        const confirmar = confirm("¿Seguro que quieres cancelar esta sesión? Se eliminará completamente.");
        if (!confirmar || !id) return;

        try {
            const res = await fetch(`http://localhost:8000/sesiones/${id}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${estado.token}`,
                },
            });

            if (!res.ok) throw new Error("Error al eliminar la sesión");

            alert("✅ Sesión cancelada y eliminada.");
            navigate("/dashboard"); // o "/rutinas" según tu flujo
        } catch (err) {
            console.error(err);
            alert("❌ Error al cancelar la sesión.");
        }
    };
    const handleDragEnd = (result: DropResult) => {
        if (!result.destination || result.destination.index === result.source.index) return;
        const copia = [...ejercicios];
        const [movido] = copia.splice(result.source.index, 1);
        copia.splice(result.destination.index, 0, movido);
        setEjercicios(copia.map((e, i) => ({ ...e, orden: i + 1 })));
    };

    return (
        <div className="min-h-screen bg-gray-100 pt-24 px-6">
            <Navbar />
            <div className="max-w-3xl mx-auto">
                <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">Sesión de entrenamiento</h1>
                {sesion && (
                    <div className="text-center text-gray-600 mb-6">
                        <p>
                            <span className="font-semibold">Rutina:</span>{" "}
                            {sesion.nombre_rutina || "Sin rutina vinculada"}
                        </p>
                        <p>
                            <span className="font-semibold">Fecha:</span>{" "}
                            {new Date(sesion.fecha).toLocaleDateString()}
                        </p>
                    </div>
                )}

                {ejercicios.length === 0 ? (
                    <p className="text-center text-gray-500">Cargando ejercicios...</p>
                ) : (
                    <>
                        <DragDropContext onDragEnd={handleDragEnd}>
                            <Droppable droppableId="ejercicios-droppable">
                                {(provided) => (
                                    <div ref={provided.innerRef} {...provided.droppableProps}>
                                        {ejercicios.map((ej, i) => (
                                            <Draggable key={ej.id} draggableId={ej.id.toString()} index={i}>
                                                {(provided) => (
                                                    <div
                                                        ref={provided.innerRef}
                                                        {...provided.draggableProps}
                                                        {...provided.dragHandleProps}
                                                        className="bg-white p-4 rounded shadow mb-4"
                                                    >
                                                        <div className="flex justify-between items-center">
                                                            <h2 className="font-semibold text-blue-700 text-lg">{ej.ejercicio.nombre}</h2>
                                                            <button
                                                                onClick={() => eliminarEjercicio(ej.id)}
                                                                className="text-red-600 text-sm hover:underline"
                                                            >
                                                                🗑 Eliminar ejercicio
                                                            </button>
                                                        </div>

                                                        <p className="text-sm text-gray-500 mb-2">Grupo: {ej.ejercicio.grupo_muscular}</p>

                                                        <div className="grid grid-cols-4 font-semibold text-sm mt-2 text-gray-600">
                                                            <span>Serie</span>
                                                            <span>Peso</span>
                                                            <span>Reps</span>
                                                            <span></span>
                                                        </div>

                                                        {ej.series_detalle.map((s, idx) => (
                                                            <div
                                                                key={s.id}
                                                                className={`grid grid-cols-5 gap-2 my-1 items-center ${s.completada ? 'bg-green-100' : ''}`}
                                                            >
                                                                <span className="text-sm">{s.numero}</span>
                                                                <input
                                                                    type="number"
                                                                    min={0}
                                                                    value={s.peso === null || isNaN(s.peso) ? "" : s.peso}
                                                                    onChange={(e) => {
                                                                        const copia = [...ejercicios];
                                                                        copia[i].series_detalle[idx].peso = e.target.value === "" ? 0 : parseFloat(e.target.value);
                                                                        setEjercicios(copia);
                                                                    }}
                                                                    className="border rounded p-1"
                                                                />
                                                                <input
                                                                    type="number"
                                                                    min={0}
                                                                    value={s.repeticiones === null || isNaN(s.repeticiones) ? "" : s.repeticiones}
                                                                    onChange={(e) => {
                                                                        const copia = [...ejercicios];
                                                                        copia[i].series_detalle[idx].repeticiones = e.target.value === "" ? 0 : parseInt(e.target.value);
                                                                        setEjercicios(copia);
                                                                    }}
                                                                    className="border rounded p-1"
                                                                />
                                                                <button
                                                                    onClick={() => {
                                                                        const copia = [...ejercicios];
                                                                        copia[i].series_detalle[idx].completada = !copia[i].series_detalle[idx].completada;
                                                                        setEjercicios(copia);
                                                                    }}
                                                                    className={`text-xs px-2 py-1 rounded ${s.completada ? "bg-green-600 text-white" : "bg-gray-300 text-gray-800"}`}
                                                                >
                                                                    {s.completada ? "✔" : "Marcar"}
                                                                </button>
                                                                <button
                                                                    onClick={() => eliminarSerie(s.id, i, idx)}
                                                                    className="text-red-600 hover:underline text-sm"
                                                                >
                                                                    🗑
                                                                </button>
                                                            </div>
                                                        ))}

                                                        <button
                                                            onClick={() => añadirSerie(ej.id, i)}
                                                            className="text-sm text-green-600 hover:underline mt-2"
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


                        <div className="bg-white p-4 rounded shadow mt-8">
                            <h2 className="text-lg font-semibold text-gray-700 mb-4">➕ Añadir nuevo ejercicio</h2>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                                <input
                                    type="text"
                                    placeholder="Buscar por nombre"
                                    value={filtro}
                                    onChange={(e) => setFiltro(e.target.value)}
                                    className="border px-3 py-2 rounded w-full"
                                />

                                <select
                                    value={grupoSeleccionado}
                                    onChange={(e) => setGrupoSeleccionado(e.target.value)}
                                    className="border px-3 py-2 rounded w-full"
                                >
                                    <option value="">Todos los grupos</option>
                                    {[...new Set(ejerciciosDisponibles.map(e => e.grupo_muscular))].map(g => (
                                        <option key={g} value={g}>{g}</option>
                                    ))}
                                </select>

                                <select
                                    value={tipoSeleccionado}
                                    onChange={(e) => setTipoSeleccionado(e.target.value)}
                                    className="border px-3 py-2 rounded w-full"
                                >
                                    <option value="">Todos los equipos</option>
                                    {[...new Set(ejerciciosDisponibles.map(e => e.tipo_equipo))].map(t => (
                                        <option key={t} value={t}>{t}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="max-h-40 overflow-y-auto border rounded">
                                {ejerciciosDisponibles
                                    .filter(e =>
                                        (filtro === "" || e.nombre.toLowerCase().includes(filtro.toLowerCase())) &&
                                        (grupoSeleccionado === "" || e.grupo_muscular === grupoSeleccionado) &&
                                        (tipoSeleccionado === "" || e.tipo_equipo === tipoSeleccionado)
                                    )
                                    .sort((a, b) => a.nombre.localeCompare(b.nombre)) // ✅ orden alfabético
                                    .map((e) => (
                                        <div
                                            key={e.id}
                                            onClick={() => setEjercicioSeleccionado(e)}
                                            className={`px-3 py-2 cursor-pointer hover:bg-gray-200 ${ejercicioSeleccionado?.id === e.id ? "bg-green-100 font-bold" : ""
                                                }`}
                                        >
                                            {e.nombre} ({e.grupo_muscular} - {e.tipo_equipo})
                                        </div>
                                    ))}

                            </div>

                            {ejercicioSeleccionado && (
                                <div className="mt-3 text-sm text-green-600">
                                    ✅ Seleccionado: {ejercicioSeleccionado.nombre}
                                </div>
                            )}

                            <button
                                onClick={agregarEjercicio}
                                className="mt-4 bg-green-600 text-white px-4 py-2 rounded w-full hover:bg-green-700"
                                disabled={!ejercicioSeleccionado}
                            >
                                Añadir a la sesión
                            </button>


                        </div>
                    </>
                )}
            </div>
            <div className="text-center mt-4 flex justify-center gap-4">
                <button
                    onClick={finalizarSesion}
                    className="bg-blue-700 hover:bg-blue-800 text-white px-6 py-2 rounded"
                >
                    Finalizar sesión y actualizar rutina base
                </button>
                <button
                    onClick={cancelarSesion}
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded"
                >
                    Cancelar sesión
                </button>
            </div>
        </div>
    );
}
