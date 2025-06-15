import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { PhotoProvider, PhotoView } from "react-photo-view";
import "react-photo-view/dist/react-photo-view.css";



interface Foto {
    id: number;
    ruta: string;
}

interface Progreso {
    id: number;
    fecha: string;
    peso: number;
    comentarios?: string | null;
    fotos: Foto[];
}

export default function ProgresoDetalle() {
    const { estado } = useAuth();
    const { id } = useParams();
    const navigate = useNavigate();
    const [progreso, setProgreso] = useState<Progreso | null>(null);
    const [peso, setPeso] = useState<number>(0);
    const [comentarios, setComentarios] = useState<string>("");

    useEffect(() => {
        fetch(`http://localhost:8000/progresos/${id}`, {
            headers: { Authorization: `Bearer ${estado.token}` },
        })
            .then((res) => res.json())
            .then((data) => {
                setProgreso(data);
                setPeso(data.peso);
                setComentarios(data.comentarios || "");
            });
    }, [id, estado.token]);

    const guardarCambios = async () => {
        await fetch(`http://localhost:8000/progresos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${estado.token}`,
            },
            body: JSON.stringify({ peso, comentarios }),
        });
        alert("Cambios guardados");
    };

    const eliminarFoto = async (fotoId: number) => {
        const confirmar = confirm("¿Eliminar esta foto?");
        if (!confirmar) return;

        await fetch(`http://localhost:8000/progresos/fotos/${fotoId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${estado.token}` },
        });

        setProgreso((prev) =>
            prev ? { ...prev, fotos: prev.fotos.filter((f) => f.id !== fotoId) } : null
        );
    };
    const subirFotos = async (files: FileList) => {
        if (!progreso) return;

        const existentes = progreso.fotos.length;
        const nuevos = files.length;

        if (existentes + nuevos > 10) {
            alert("No puedes subir más de 10 fotos en total");
            return;
        }

        const formData = new FormData();
        Array.from(files).forEach((f) => formData.append("archivos", f));

        const res = await fetch(`http://localhost:8000/progresos/${id}/fotos`, {
            method: "POST",
            headers: { Authorization: `Bearer ${estado.token}` }, // ❌ NO pongas Content-Type
            body: formData,
        });

        if (!res.ok) {
            alert("Error al subir las fotos");
            return;
        }

        const nuevas = await res.json();
        setProgreso((prev) =>
            prev ? { ...prev, fotos: [...prev.fotos, ...nuevas] } : null
        );
    };


    const eliminarProgreso = async () => {
        const confirmar = confirm("¿Eliminar todo el progreso?");
        if (!confirmar) return;

        await fetch(`http://localhost:8000/progresos/${id}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${estado.token}` },
        });

        alert("Progreso eliminado");
        navigate("/progreso");
    };

    if (!progreso) return <div className="pt-24 text-center">Cargando...</div>;

    return (
        <div className="min-h-screen bg-gray-100 pt-24 px-6">
            <Navbar />
            <div className="max-w-2xl mx-auto bg-white p-6 rounded shadow">
                <div className="mb-4">
                    <button
                        onClick={() => navigate(-1)}
                        className="text-blue-600 hover:underline text-sm"
                    >
                        ⬅ Volver atrás
                    </button>
                </div>

                <h1 className="text-2xl font-bold text-blue-600 mb-4">
                    Progreso del {new Date(progreso.fecha).toLocaleDateString()}
                </h1>

                <div className="mb-4">
                    <label className="font-semibold">Peso (kg):</label>
                    <input
                        type="number"
                        value={peso}
                        onChange={(e) => setPeso(parseFloat(e.target.value))}
                        className="w-full border rounded px-3 py-2 mt-1"
                    />
                </div>

                <div className="mb-4">
                    <label className="font-semibold">Comentarios:</label>
                    <textarea
                        value={comentarios}
                        onChange={(e) => setComentarios(e.target.value)}
                        rows={3}
                        className="w-full border rounded px-3 py-2 mt-1"
                    />
                </div>

                <div className="mb-4">
                    <label className="font-semibold block mb-1">Fotos:</label>
                    <PhotoProvider>
                        <div className="grid grid-cols-2 gap-4">
                            {progreso.fotos.map((f) => (
                                <PhotoView key={f.id} src={`http://localhost:8000/static/${f.ruta}`}>
                                    <div className="relative cursor-zoom-in">
                                        <img
                                            src={`http://localhost:8000/static/${f.ruta}`}
                                            alt="foto progreso"
                                            className="w-full rounded shadow"
                                        />
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation(); // ⛔️ evita que se abra el zoom
                                                eliminarFoto(f.id);
                                            }}
                                            className="absolute top-1 right-1 bg-red-600 text-white rounded px-2 py-1 text-xs"
                                        >
                                            🗑
                                        </button>
                                    </div>
                                </PhotoView>
                            ))}
                        </div>
                    </PhotoProvider>
                </div>


                <div className="mt-4">
                    <label className="block font-semibold mb-1">Añadir más fotos:</label>
                    <input
                        type="file"
                        accept="image/*"
                        multiple
                        onChange={(e) => {
                            if (e.target.files) subirFotos(e.target.files);
                            e.target.value = ""; // limpia el input tras cada subida
                        }}
                    />
                    <p className="text-xs text-gray-500">Máximo 10 imágenes en total por progreso.</p>
                </div>

                <div className="flex gap-4 mt-4 justify-end">
                    <button
                        onClick={guardarCambios}
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                        Guardar cambios
                    </button>
                    <button
                        onClick={eliminarProgreso}
                        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                    >
                        Eliminar progreso
                    </button>
                </div>
            </div>
        </div>
    );
}
