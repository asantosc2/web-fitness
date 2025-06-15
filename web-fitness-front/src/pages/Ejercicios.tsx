//ejercicio.tsx
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

interface Ejercicio {
  id: number;
  nombre: string;
  grupo_muscular: string;
  tipo_equipo: string;
  imagen_url?: string | null;
}

export default function Ejercicios() {
  const { estado } = useAuth();
  const [ejercicios, setEjercicios] = useState<Ejercicio[]>([]);
  const [grupoFiltro, setGrupoFiltro] = useState<string>("");
  const [equipoFiltro, setEquipoFiltro] = useState<string>("");
  const [nombreFiltro, setNombreFiltro] = useState<string>("");
  const navigate = useNavigate();

  const grupos = Array.from(new Set(ejercicios.map(e => e.grupo_muscular)));
  const equipos = Array.from(new Set(ejercicios.map(e => e.tipo_equipo)));

  const ejerciciosOrdenados = [...ejercicios].sort((a, b) =>
    a.nombre.localeCompare(b.nombre)
  );

  const ejerciciosFiltrados = ejerciciosOrdenados.filter(ej =>
    (grupoFiltro === "" || ej.grupo_muscular === grupoFiltro) &&
    (equipoFiltro === "" || ej.tipo_equipo === equipoFiltro) &&
    (nombreFiltro === "" || ej.nombre.toLowerCase().includes(nombreFiltro.toLowerCase()))
  );

  useEffect(() => {
    fetch("http://localhost:8000/ejercicios", {
      headers: {
        Authorization: `Bearer ${estado.token}`,
      },
    })
      .then(res => res.json())
      .then(data => setEjercicios(data))
      .catch(err => console.error("Error cargando ejercicios:", err));
  }, [estado.token]);

  return (
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <h1 className="text-3xl font-bold text-blue-600 mb-8 text-center">
        Listado de ejercicios
      </h1>

      <div className="max-w-6xl mx-auto mb-8 grid gap-4 grid-cols-1 md:grid-cols-4">
        <input
          type="text"
          placeholder="Buscar por nombre"
          value={nombreFiltro}
          onChange={e => setNombreFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm col-span-1"
        />
        <select
          value={grupoFiltro}
          onChange={e => setGrupoFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm col-span-1"
        >
          <option value="">Todas las partes del cuerpo</option>
          {grupos.map(grupo => (
            <option key={grupo} value={grupo}>{grupo}</option>
          ))}
        </select>

        <select
          value={equipoFiltro}
          onChange={e => setEquipoFiltro(e.target.value)}
          className="border px-3 py-2 rounded shadow-sm col-span-1"
        >
          <option value="">Todas las categorías</option>
          {equipos.map(equipo => (
            <option key={equipo} value={equipo}>{equipo}</option>
          ))}
        </select>

        <button
          onClick={() => navigate("/ejercicios/nuevo")}
          className="bg-blue-600 text-white font-semibold px-4 py-2 rounded shadow hover:bg-blue-700 transition col-span-1"
        >
          Añadir ejercicio
        </button>
      </div>

      {/* Ejercicios en líneas horizontales */}
      <div className="max-w-4xl mx-auto flex flex-col gap-2">
        {ejerciciosFiltrados.map(ej => (
          <div
            key={ej.id}
            className="bg-white rounded-lg shadow p-2 flex items-center justify-between gap-4"
          >
            <div className="flex items-center gap-4">
              {ej.imagen_url ? (
                <img
                  src={ej.imagen_url}
                  alt={ej.nombre}
                  className="w-20 h-20 object-cover rounded"
                />
              ) : (
                <div className="w-20 h-20 bg-gray-200 flex items-center justify-center rounded text-gray-500">
                  Sin imagen
                </div>
              )}
              <div>
                <h2 className="text-lg font-semibold text-gray-800">{ej.nombre}</h2>
                <p className="text-sm text-gray-500">{ej.grupo_muscular}</p>
              </div>
            </div>
            <p className="text-sm text-gray-500 mr-4">Categoría: {ej.tipo_equipo}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
