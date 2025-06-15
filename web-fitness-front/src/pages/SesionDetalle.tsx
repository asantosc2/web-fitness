// src/pages/SesionDetalle.tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";


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

    const actualizarSerie = async (
        ejercicioIndex: number,
        serieIndex: number,
        campo: "peso" | "repeticiones",
        valor: number
    ) => {
        const copia = [...ejercicios];
        const serie = copia[ejercicioIndex].series_detalle[serieIndex];
        serie[campo] = valor;
        setEjercicios(copia);

        await fetch(`http://localhost:8000/sesion-serie/${serie.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${estado.token}`,
            },
            body: JSON.stringify({ [campo]: valor }),
        });
    };

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

    const finalizarSesion = async () => {
        const confirmar = confirm("¿Deseas finalizar esta sesión y actualizar la rutina base?");
        if (!confirmar || !id) return;

        try {
            const res = await fetch(`http://localhost:8000/sesiones/${id}/actualizar-rutina`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${estado.token}`,
                },
            });

            if (!res.ok) throw new Error("Error al actualizar la rutina");

            alert("✅ Rutina actualizada correctamente.");
            navigate("/rutinas"); // Puedes cambiar la ruta a donde quieras redirigir
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



    return (
        <div className="min-h-screen bg-gray-100 pt-24 px-6">
            <Navbar />
            <div className="max-w-3xl mx-auto">
                <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">Sesión de entrenamiento</h1>

                {ejercicios.length === 0 ? (
                    <p className="text-center text-gray-500">Cargando ejercicios...</p>
                ) : (
                    <>
                        {ejercicios.map((ej, i) => (
                            <div key={ej.id} className="bg-white p-4 rounded shadow mb-4">
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
                                    <div key={s.id} className={`grid grid-cols-5 gap-2 my-1 items-center ${s.completada ? 'bg-green-100' : ''}`}>
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
                        ))}

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
